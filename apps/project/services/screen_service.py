from rest_framework.exceptions import ValidationError

from ..models import Screen


class ScreenService:

    @staticmethod
    def get_all_screens():

        return Screen.objects.filter(
            deleted_at__isnull=True
        )

    @staticmethod
    def create_screen(user, data):

        code = data.get(
            "code",
            ""
        ).upper()

        module = data.get("module")

        # Prevent duplicate screen code
        # inside same module

        existing_screen = Screen.objects.filter(

            module=module,

            code=code,

            deleted_at__isnull=True

        ).exists()

        if existing_screen:

            raise ValidationError({
                "code": (
                    "Screen code already "
                    "exists in this module."
                )
            })

        return Screen.objects.create(

            module=module,

            name=data.get("name"),

            description=data.get(
                "description"
            ),

            code=code,

            created_by=user,
            updated_by=user,
        )

    @staticmethod
    def update_screen(screen, user, data):

        code = data.get(
            "code",
            screen.code
        ).upper()

        module = data.get(
            "module",
            screen.module
        )

        # Prevent duplicate code
        # inside same module

        existing_screen = Screen.objects.filter(

            module=module,

            code=code,

            deleted_at__isnull=True

        ).exclude(
            uuid=screen.uuid
        ).exists()

        if existing_screen:

            raise ValidationError({
                "code": (
                    "Screen code already "
                    "exists in this module."
                )
            })

        screen.module = module

        screen.name = data.get(
            "name",
            screen.name
        )

        screen.description = data.get(
            "description",
            screen.description
        )

        screen.code = code

        screen.updated_by = user

        screen.save()

        return screen

    @staticmethod
    def delete_screen(screen):

        screen.delete()