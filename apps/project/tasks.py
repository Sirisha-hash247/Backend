from .models import TestCase

def bulk_import_testcases_task(data, user_id):
    created = 0
    errors = []

    for i, row in enumerate(data):
        try:
            TestCase.objects.create(
                title=row.get("title"),
                description=row.get("description"),
                expected_results=row.get("expected_results"),
                priority=row.get("priority", "medium"),
                status=row.get("status", "open"),
                screen_id=row.get("screen"),
                created_by_id=user_id,
                updated_by_id=user_id,
            )
            created += 1

        except Exception as e:
            errors.append(f"Row {i+1}: {str(e)}")

    return {
        "created": created,
        "errors": errors
    }