from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organization


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'username', 'role', 'organization', 'is_staff', 'is_active')
    list_filter = ('role', 'organization', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'organization')}),  # 🔥 ADDED
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'role',
                'organization',   # 🔥 ADDED HERE ALSO
                'is_staff',
                'is_active'
            ),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'domain', 'created_at')
    search_fields = ('name', 'domain')