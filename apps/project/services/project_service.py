from apps.project.models import Project
from django.utils.timezone import now

def create_project(user, validated_data):
    return Project.objects.create(
        created_by=user,
        updated_by=user,
        **validated_data
    )


def get_all_projects():
    return Project.objects.filter(deleted_at__isnull=True)

def update_project(project, validated_data, user):
    for attr, value in validated_data.items():
        setattr(project, attr, value)

    project.updated_by = user
    project.save()
    return project

def delete_project(project, user):
    from django.utils.timezone import now

    project.deleted_at = now()
    project.deleted_by = user
    project.save()