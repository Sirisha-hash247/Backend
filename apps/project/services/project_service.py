from apps.project.models import Project
from django.utils.timezone import now


# ✅ CREATE (WITH ORG)
def create_project(user, validated_data):
    return Project.objects.create(
        organization=user.organization,   # 🔥 ADD THIS
        created_by=user,
        updated_by=user,
        **validated_data
    )


# ✅ FILTER BY ORG
def get_all_projects(user):
    if user.role == "superadmin":
        return Project.objects.filter(deleted_at__isnull=True)

    return Project.objects.filter(
        organization=user.organization,
        deleted_at__isnull=True
    )


# ✅ UPDATE (WITH ORG CHECK)
def update_project(project, user, validated_data):
    # 🔒 Prevent cross-org update
    if user.role != "superadmin" and project.organization != user.organization:
        raise PermissionError("You cannot update this project")

    for attr, value in validated_data.items():
        setattr(project, attr, value)

    project.updated_by = user
    project.save()
    return project


# ✅ DELETE (WITH ORG CHECK)
def delete_project(project, user):
    if user.role != "superadmin" and project.organization != user.organization:
        raise PermissionError("You cannot delete this project")

    project.deleted_at = now()
    project.deleted_by = user
    project.save()