from apps.project.models import (
    TestRunVersion,
    TestCase,
    TestRun,
    Screen,
)


class TestRunVersionService:

    @staticmethod
    def create_version(data, user):

        screen = Screen.objects.get(
            uuid=data["screen"]
        )

        module = screen.module

        project = module.project

        # ============================================
        # AUTO VERSION NUMBER
        # ============================================

        existing_versions_count = (
            TestRunVersion.objects.filter(
                screen=screen,
                deleted_at__isnull=True
            ).count()
        )

        next_version_number = (
            f"v{existing_versions_count + 1}"
        )

        # ============================================
        # CREATE VERSION
        # ============================================

        version = TestRunVersion.objects.create(

            project=project,

            module=module,

            screen=screen,

            version_number=next_version_number,

            version_status="draft",

            notes=f"Snapshot for {next_version_number}",

            created_by=user,

            updated_by=user,
        )

        # ============================================
        # GET ALL CURRENT TESTCASES
        # ============================================

        testcases = TestCase.objects.filter(

            screen=screen,

            deleted_at__isnull=True

        ).order_by("display_order")

        test_run_objects = []

        # ============================================
        # COPY CURRENT TESTCASE PAGE
        # ============================================

        for testcase in testcases:

            test_run_objects.append(

                TestRun(

                    project=project,

                    module=module,

                    screen=screen,

                    version=version,

                    testcase=testcase,

                    title=testcase.title,

                    description=testcase.description,

                    expected_results=testcase.expected_results,

                    steps=testcase.steps,

                    priority=testcase.priority,

                    type_of_testcase=testcase.type_of_testcase,

                    display_order=testcase.display_order,

                    created_by=user,

                    updated_by=user,
                )

            )

        # ============================================
        # CREATE TEST RUNS
        # ============================================

        TestRun.objects.bulk_create(
            test_run_objects
        )

        return version