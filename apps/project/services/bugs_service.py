from rest_framework.exceptions import ValidationError

from apps.project.models import (
    Bug,
    Project,
    Module,
    Screen,
    TestCase,
)


class BugService:

    # =====================================================
    # GENERATE BUG ID
    # Example:
    # B-AUTH-SIGNUP-001
    # =====================================================

    @staticmethod
    def generate_bug_id(screen):

        module_code = (
            screen.module.code.upper()
        )

        screen_code = (
            screen.code.upper()
        )

        last_bug = (

            Bug.objects.filter(
                screen=screen
            )

            .exclude(
                bug_id__isnull=True
            )

            .order_by("-bug_id")

            .first()
        )

        next_sequence = 1

        if (
            last_bug
            and last_bug.bug_id
        ):

            try:

                last_sequence = int(

                    last_bug.bug_id
                    .split("-")[-1]
                )

                next_sequence = (
                    last_sequence + 1
                )

            except:

                next_sequence = 1

        return (

            f"B-"

            f"{module_code}-"

            f"{screen_code}-"

            f"{str(next_sequence).zfill(3)}"
        )

    # =====================================================
    # CREATE BUG
    # =====================================================

    @staticmethod
    def create_bug(user, data):

        try:

            # -------- REQUIRED FIELDS --------

            required_fields = [

                "project",

                "module",

                "screen",

                "description",

                "steps_to_reproduce",

                "severity",

                "expected_results",

                "actual_result",
                
                
                "issue_type",
            ]

            for field in required_fields:

                if (
                    field not in data
                    or data[field] in [None, ""]
                ):

                    raise ValidationError(
                        f"{field} is required"
                    )

            # -------- FETCH PROJECT --------

            try:

                project = Project.objects.get(
                    uuid=data["project"]
                )

            except Project.DoesNotExist:

                raise ValidationError(
                    "Invalid project"
                )

            # -------- FETCH MODULE --------

            try:

                module = Module.objects.get(
                    uuid=data["module"]
                )

            except Module.DoesNotExist:

                raise ValidationError(
                    "Invalid module"
                )

            # -------- FETCH SCREEN --------

            try:

                screen = Screen.objects.get(
                    uuid=data["screen"]
                )

            except Screen.DoesNotExist:

                raise ValidationError(
                    "Invalid screen"
                )

            # -------- FETCH TESTCASE --------

            testcase = None

            if data.get("testcase"):

                try:

                    testcase = TestCase.objects.get(
                        uuid=data["testcase"]
                    )

                except TestCase.DoesNotExist:

                    raise ValidationError(
                        "Invalid testcase"
                    )

            # =====================================================
            # GENERATE BUG ID
            # =====================================================

            bug_id = (
                BugService.generate_bug_id(
                    screen
                )
            )

            # =====================================================
            # CREATE BUG
            # =====================================================

            bug = Bug.objects.create(

                bug_id=bug_id,

                project=project,

                module=module,

                screen=screen,

                testcase=testcase,

                test_cycle_id=data.get(
                    "test_cycle_id"
                ),

                description=data[
                    "description"
                ],

                steps_to_reproduce=data[
                    "steps_to_reproduce"
                ],

                severity=data[
                    "severity"
                ],

                expected_results=data[
                    "expected_results"
                ],

                actual_result=data[
                    "actual_result"
                ],

                status=data.get(
                    "status",
                    "open"
                ),
                
                issue_type=data.get(
    "issue_type"
),

                screenshot_id=data.get(
                    "screenshot_id"
                ),

                created_by=user,

                updated_by=user,
            )

            return bug

        except Exception as e:

            raise ValidationError(str(e))