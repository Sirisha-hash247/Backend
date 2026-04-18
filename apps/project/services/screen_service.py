from ..models import Screen


class ScreenService:

    @staticmethod
    def get_all_screens():
        return Screen.objects.all()

    @staticmethod
    def create_screen(user, data):
        return Screen.objects.create(
            created_by=user,
            updated_by=user,
            **data
        )

    @staticmethod
    def update_screen(screen, user, data):
        for key, value in data.items():
            setattr(screen, key, value)

        screen.updated_by = user
        screen.save()
        return screen

    @staticmethod
    def delete_screen(screen):
        screen.delete()