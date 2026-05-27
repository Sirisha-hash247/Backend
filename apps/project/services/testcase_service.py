from django.utils import timezone

from rest_framework.exceptions import ValidationError

from apps.project.models import (
    TestCase,
    Screen
)

from apps.users.models import User


class TestCaseService:

    # ============================================
    # GENERATE TC ID
    # ============================================

    @staticmethod
    def generate_tc_id(screen):

        module_code = (
            screen.module.code.upper()
        )

        screen_code = (
            screen.code.upper()
        )

        last_testcase = (

            TestCase.objects.filter(
                screen=screen
            )

            .exclude(
                tc_id__isnull=True
            )

            .exclude(
                tc_id=""
            )

            .order_by("-tc_id")

            .first()
        )

        next_sequence = 1

        if (
            last_testcase
            and last_testcase.tc_id
        ):

            try:

                last_sequence = int(

                    last_testcase.tc_id
                    .split("-")[-1]
                )

                next_sequence = (
                    last_sequence + 1
                )

            except Exception:

                next_sequence = 1

        return (

            f"TC-"

            f"{module_code}-"

            f"{screen_code}-"

            f"{str(next_sequence).zfill(3)}"
        )

    # ============================================
    # CREATE TESTCASE
    # ============================================

    @staticmethod
    def create_testcase(user, data):
        """
        Create a new TestCase
        """

        try:

            # ---------------- REQUIRED FIELDS ----------------

            required_fields = [
                "title",
                "description",
                "expected_results",
                "priority",
                "type_of_testcase",
                "screen",
            ]

            for field in required_fields:

                if (
                    field not in data
                    or data[field] in [None, ""]
                ):

                    raise ValidationError(
                        f"{field} is required"
                    )

            # ---------------- SCREEN FETCH ----------------

            screen = data["screen"]

            # ---------------- ASSIGNED USER (OPTIONAL) ----------------

            assigned_user = data.get(
                 "assigned_to"
            )

            # ---------------- STEPS ----------------

            steps = data.get("steps", {})

            # ---------------- GENERATE TC ID ----------------

            tc_id = (
                TestCaseService.generate_tc_id(
                    screen
                )
            )

            # ---------------- CREATE TESTCASE ----------------

            testcase = TestCase.objects.create(

                tc_id=tc_id,

                screen=screen,

                title=data["title"],

                description=data["description"],

                expected_results=data[
                    "expected_results"
                ],

                priority=data["priority"],

                status=data.get(
                    "status",
                    "open"
                ),

                type_of_testcase=data[
                    "type_of_testcase"
                ],

                assigned_to=assigned_user,

                steps=steps,

                # BaseModel fields

                created_by=user,

                updated_by=user,
            )

            return testcase

        except Exception as e:

            raise ValidationError(str(e))