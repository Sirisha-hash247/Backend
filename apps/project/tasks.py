from .models import TestCase

def bulk_import_testcases_task(data, user_id):
    created = 0
    errors = []

    for i, row in enumerate(data):
        try:
            # 🔥 HANDLE STEPS (VERY IMPORTANT)
            raw_steps = row.get("steps", [])

            if isinstance(raw_steps, list):
                steps = {
                    f"step {i+1}": step
                    for i, step in enumerate(raw_steps)
                    if str(step).strip() != ""
                }
            else:
                steps = {}

            TestCase.objects.create(
                title=row.get("title"),
                description=row.get("description"),
                expected_results=row.get("expected_results"),
                priority=row.get("priority", "medium"),
                status=row.get("status", "open"),

                # 🔥 ADD THIS (MISSING)
                type_of_testcase=row.get("type_of_testcase", "functional"),

                # 🔥 ADD THIS (MISSING)
                steps=steps,

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