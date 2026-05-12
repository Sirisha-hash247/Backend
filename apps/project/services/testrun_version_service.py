
from apps.project.models import TestRunVersion, TestCase, TestRun, Screen


class TestRunVersionService:

    @staticmethod
    def create_version(data, user):

        screen = Screen.objects.get(
            uuid=data["screen"]
        )

        module = screen.module

        project = module.project

        version = TestRunVersion.objects.create(

            project=project,
            module=module,
            screen=screen,

            version_number=data.get(
                "version_number"
            ),

            version_status=data.get(
                "version_status",
                "draft"
            ),

            notes=data.get("notes"),

            created_by=user,
            updated_by=user,
        )

        testcases = TestCase.objects.filter(
            screen=screen,
            deleted_at__isnull=True
        ).order_by("display_order")

        test_run_objects = []

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

        TestRun.objects.bulk_create(
            test_run_objects
        )

        return version