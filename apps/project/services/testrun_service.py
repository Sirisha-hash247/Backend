# services/testrun_service.py

from rest_framework.exceptions import ValidationError
from apps.project.models import TestRun, TestCase
from apps.users.models import User

def create_test_run(user, data):
    try:
        test_case = TestCase.objects.get(uuid=data["test_case"])

        return TestRun.objects.create(
            test_case=test_case,
            actual_results=data["actual_results"],
            status=data["status"],
            executed_by=user,
        )

    except TestCase.DoesNotExist:
        raise ValidationError("Invalid test case")