# services/testrun_service.py

from rest_framework.exceptions import ValidationError
from apps.project.models import TestRun, TestCase
from apps.users.models import User
from django.utils import timezone

class TestRunService:

    @staticmethod
    def get_by_version(version_id):

        return TestRun.objects.filter(
            version_id=version_id,
            deleted_at__isnull=True
        ).order_by("display_order")

    @staticmethod
    def update_test_run(test_run, data, user):

        test_run.run_status = data.get(
            "run_status",
            test_run.run_status
        )

        test_run.actual_result = data.get(
            "actual_result",
            test_run.actual_result
        )

        test_run.notes = data.get(
            "notes",
            test_run.notes
        )

        test_run.executed_by = user

        test_run.updated_by = user

        if data.get("run_status") == "in_progress":

            if not test_run.started_at:
                test_run.started_at = timezone.now()

        if data.get("run_status") in [
            "passed",
            "failed",
            "blocked"
        ]:

            test_run.completed_at = timezone.now()

        test_run.save()


        return test_run
    
    @staticmethod
    def get_by_version(version_id):

        return TestRun.objects.filter(
            version_id=version_id,
            deleted_at__isnull=True
        ).order_by("display_order")