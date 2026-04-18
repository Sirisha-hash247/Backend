from django.contrib import admin
from .models import Project, Module, Screen


# ---------------- PROJECT ADMIN ----------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_by', 'created_at')
    search_fields = ('title',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


# ---------------- MODULE ADMIN ----------------
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'project', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# ---------------- SCREEN ADMIN ----------------
@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'module', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)