from ..models import Module


from rest_framework.exceptions import ValidationError

class ModuleService:

    @staticmethod
    def get_all_modules():

        return Module.objects.filter(
            deleted_at__isnull=True
        )

    @staticmethod
    def create_module(user, data):

        code = data.get("code", "").upper()

        # Prevent duplicate codes

        if Module.objects.filter(
            code=code,
            deleted_at__isnull=True
        ).exists():

            raise ValidationError({
                "code": "Module code already exists."
            })

        return Module.objects.create(

            project=data["project"],

            name=data["name"],

            code=code,

            created_by=user,
            updated_by=user,
        )

    @staticmethod
    def update_module(module, user, data):

        code = data.get(
            "code",
            module.code
        ).upper()

        # Prevent duplicate codes

        existing_module = Module.objects.filter(
            code=code,
            deleted_at__isnull=True
        ).exclude(
            uuid=module.uuid
        ).exists()

        if existing_module:

            raise ValidationError({
                "code": "Module code already exists."
            })

        module.project = data.get(
            "project",
            module.project
        )

        module.name = data.get(
            "name",
            module.name
        )

        module.code = code

        module.updated_by = user

        module.save()

        return module

    @staticmethod
    def delete_module(module):

        module.delete()