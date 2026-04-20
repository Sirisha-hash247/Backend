from rest_framework.exceptions import ValidationError

from apps.project.models import Bug, Project, Module, Screen, TestCase


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
            "actual_results",
        ]

        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                raise ValidationError(f"{field} is required")

        # -------- FETCH RELATIONS --------
        try:
            project = Project.objects.get(id=data["project"])
        except Project.DoesNotExist:
            raise ValidationError("Invalid project")

        try:
            module = Module.objects.get(uuid=data["module"])
        except Module.DoesNotExist:
            raise ValidationError("Invalid module")

        try:
            screen = Screen.objects.get(uuid=data["screen"])
        except Screen.DoesNotExist:
            raise ValidationError("Invalid screen")

        test_case = None
        if data.get("test_case"):
            try:
                test_case = TestCase.objects.get(uuid=data["test_case"])
            except TestCase.DoesNotExist:
                raise ValidationError("Invalid test_case")

        # -------- CREATE BUG --------
        bug = Bug.objects.create(
            project=project,
            module=module,
            screen=screen,
            test_case=test_case,

            test_cycle_id=data.get("test_cycle_id"),

            description=data["description"],
            steps_to_reproduce=data["steps_to_reproduce"],

            severity=data["severity"],
            expected_results=data["expected_results"],
            actual_results=data["actual_results"],

            status=data.get("status", "open"),
            screenshot_id=data.get("screenshot_id"),

            created_by=user,
            updated_by=user,
        )

        return bug

    except Exception as e:
        raise ValidationError(str(e))