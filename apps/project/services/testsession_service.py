from apps.project.models import (
TestSession,
TestRun
)

class TestSessionService:


 @staticmethod
 def create_session(
    session,
    user
):

    previous_session = (
        TestSession.objects.filter(
            version=session.version,
            testing_type=session.testing_type,
            deleted_at__isnull=True
        )
        .exclude(
            uuid=session.uuid
        )
        .order_by("-created_at")
        .first()
    )

    # ===================================
    # GET SOURCE RUNS
    # ===================================

    source_runs = TestRun.objects.none()

    if previous_session:

        source_runs = TestRun.objects.filter(
            session=previous_session,
            deleted_at__isnull=True
        )

    # FALLBACK TO TEMPLATE RUNS

    if not source_runs.exists():

        source_runs = TestRun.objects.filter(
            version=session.version,
            session__isnull=True,
            deleted_at__isnull=True
        )

    # ===================================
    # FILTER TEST TYPE
    # ===================================

    type_mapping = {

        "Functional Testing":
        "functional",

        "Regression Testing":
        "regression",

        "Smoke Testing":
        "smoke",

        "Sanity Testing":
        "system",

        "API Testing":
        "integration",
    }

    mapped_type = type_mapping.get(
        session.testing_type
    )

    if mapped_type:

        source_runs = source_runs.filter(
            type_of_testcase=mapped_type
        )

    print(
        "SOURCE RUN COUNT:",
        source_runs.count()
    )

    new_runs = []

    for run in source_runs:

        new_runs.append(

            TestRun(

                project=run.project,
                module=run.module,
                screen=run.screen,

                version=run.version,
                session=session,

                testcase=run.testcase,

                tc_id=run.tc_id,

                title=run.title,
                description=run.description,
                expected_results=run.expected_results,

                steps=run.steps,

                priority=run.priority,

                type_of_testcase=run.type_of_testcase,

                display_order=run.display_order,

                run_status="not_started",

                actual_result="",
                notes="",

                executed_by=None,

                started_at=None,
                completed_at=None,

                created_by=user,
                updated_by=user,
            )
        )

    TestRun.objects.bulk_create(
        new_runs
    )

    print(
        "NEW RUNS CREATED:",
        len(new_runs)
    )

    return session

