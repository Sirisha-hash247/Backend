from apps.users.models import User


def get_all_users():
    return User.objects.all()