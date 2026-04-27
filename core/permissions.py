from rest_framework.permissions import BasePermission
from .roles import ROLE_ROUTES


class RoleBasedPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        role = user.role
        resource = getattr(view, "resource", None)

        if role not in ROLE_ROUTES or not resource:
            return False

        allowed_actions = ROLE_ROUTES[role].get(resource, [])

        # Map HTTP methods to actions
        method_map = {
            "GET": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete",
        }

        action = method_map.get(request.method)

        return action in allowed_actions


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "superadmin"
        )
    
class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "superadmin"]
        )
        
        
class IsTester(BasePermission):
    """Tester can do everything EXCEPT delete (except bugs)."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "tester"
        )


class IsReviewer(BasePermission):
    """Reviewer can only read."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "reviewer"
        )


class IsAdminOrTester(BasePermission):
    """Used for Module, Screen, TestCase, TestRun — CRU for both."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "tester"]
        )


class IsAdminTesterOrReviewer(BasePermission):
    """Reviewer gets read-only. Admin/Tester get full CRU."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "tester", "reviewer"]
        )