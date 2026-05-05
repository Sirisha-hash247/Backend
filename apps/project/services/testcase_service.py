from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.project.models import TestCase, Screen
from apps.users.models import User


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
            "status",
            "type_of_testcase",
            "screen",
        ]

        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                raise ValidationError(f"{field} is required")

        # ---------------- SCREEN FETCH ----------------
        try:
            screen = Screen.objects.get(uuid=data["screen"])
        except Screen.DoesNotExist:
            raise ValidationError("Invalid screen UUID")

        # ---------------- ASSIGNED USER (OPTIONAL) ----------------
        assigned_user = None
        if data.get("assigned_to"):
            try:
                assigned_user = User.objects.get(id=data["assigned_to"])
            except User.DoesNotExist:
                raise ValidationError("Invalid assigned_to user")


        steps = data.get("steps", {})
        # ---------------- CREATE TESTCASE ----------------
        testcase = TestCase.objects.create(
            screen=screen,
            title=data["title"],
            description=data["description"],
            expected_results=data["expected_results"],
            priority=data["priority"],
            status=data["status"],
            type_of_testcase=data["type_of_testcase"],
            assigned_to=assigned_user,
            
            steps=steps,

            # BaseModel fields
            created_by=user,
            updated_by=user,
        )

        return testcase

    except Exception as e:
        raise ValidationError(str(e))