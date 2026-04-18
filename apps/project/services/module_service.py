from ..models import Module


class ModuleService:

    @staticmethod
    def get_all_modules():
        return Module.objects.all()

    @staticmethod
    def create_module(user, data):
        return Module.objects.create(
            created_by=user,
            updated_by=user,
            **data
        )

    @staticmethod
    def update_module(module, user, data):
        for key, value in data.items():
            setattr(module, key, value)

        module.updated_by = user
        module.save()
        return module

    @staticmethod
    def delete_module(module):
        module.delete()