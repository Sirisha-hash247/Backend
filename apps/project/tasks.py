from .models import TestCase, Screen

def bulk_import_testcases_task(data, user_id):

    print("TASK STARTED")

    created = 0
    errors = []

    for i, row in enumerate(data):

        print("ROW:", row)

        try:

            raw_steps = row.get("steps", [])

            if isinstance(raw_steps, list):
                steps = {
                    f"Step {idx+1}": step
                    for idx, step in enumerate(raw_steps)
                    if str(step).strip() != ""
                }
            else:
                steps = {}

            print("STEPS:", steps)

            # 🔥 CHECK SCREEN
            print("SCREEN UUID:", row.get("screen"))

            screen = Screen.objects.get(uuid=row.get("screen"))

            print("SCREEN FOUND")

            testcase = TestCase.objects.create(
                title=row.get("title"),
                description=row.get("description"),
                expected_results=row.get("expected_results"),
                priority=row.get("priority", "medium"),
                status=row.get("status", "open"),
                type_of_testcase=row.get("type_of_testcase", "functional"),
                steps=steps,
                screen=screen,
                created_by_id=user_id,
                updated_by_id=user_id,
            )

            print("CREATED TESTCASE:", testcase)

            created += 1

        except Exception as e:

            print("FULL ERROR:")
            print(str(e))

            errors.append(f"Row {i+1}: {str(e)}")

    print("FINAL CREATED:", created)
    print("FINAL ERRORS:", errors)

    return {
        "created": created,
        "errors": errors
    }