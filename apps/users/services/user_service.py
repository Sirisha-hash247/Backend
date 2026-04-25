from apps.users.models import User


def get_all_users(user):
    if user.role == "superadmin":
        return User.objects.all()

    return User.objects.filter(organization=user.organization)