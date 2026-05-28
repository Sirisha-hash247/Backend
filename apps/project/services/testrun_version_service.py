from apps.project.models import (
    TestRunVersion,
    TestCase,
    TestRun,
    Screen,
)


class TestRunVersionService:

    @staticmethod
    def get_latest_version(screen_id):

        return TestRunVersion.objects.filter(
            screen_id=screen_id,
            deleted_at__isnull=True
        ).order_by("-created_at").first()

    @staticmethod
    def create_version(data, user):

    # ============================================
    # FETCH SCREEN
    # ============================================

        screen = Screen.objects.get(
            uuid=data["screen"]
        )

    # ============================================
    # GET PROJECT & MODULE FROM USER SELECTION
    # ============================================

        project_id = data.get("project")

        module_id = data.get("module")

    # ============================================
    # VALIDATION
    # ============================================

        if not project_id:

            raise Exception(
                "Project is required"
            )

        if not module_id:

            raise Exception(
                "Module is required"
            )

    # ============================================
    # CREATE VERSION
    # ============================================

        version = TestRunVersion.objects.create(

            project_id=project_id,

            module_id=module_id,

            screen=screen,

            version_number=data[
                "version_number"
            ],

            version_status=data.get(
                "version_status",
                "draft"
            ),

            notes=data.get(
                "notes",
                ""
            ),

            created_by=user,

            updated_by=user,
        )

    # ============================================
    # GET TESTCASES
    # ============================================

        testcases = TestCase.objects.filter(

            screen=screen,

            deleted_at__isnull=True

        ).order_by("display_order")

        test_run_objects = []

    # ============================================
    # COPY TESTCASES INTO TESTRUNS
    # ============================================

        for testcase in testcases:

            test_run_objects.append(

                TestRun(

                    project_id=project_id,

                    module_id=module_id,

                    screen=screen,

                    version=version,

                    testcase=testcase,

                    tc_id=testcase.tc_id,

                    title=testcase.title,

                    description=testcase.description,

                    expected_results=
                    testcase.expected_results,

                    steps=testcase.steps,

                    priority=testcase.priority,

                    type_of_testcase=
                    testcase.type_of_testcase,

                    display_order=
                    testcase.display_order,

                    created_by=user,

                    updated_by=user,
                )

            )

    # ============================================
    # BULK CREATE TESTRUNS
    # ============================================

        TestRun.objects.bulk_create(
            test_run_objects
        )

        return version