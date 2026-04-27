# apps/users/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserListView, MeView  # ✅ import MeView

urlpatterns = [
    # AUTH
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    # ✅ NEW — /api/users/me/
    path('me/', MeView.as_view()),

    path('manage/', UserListView.as_view()),
    path('manage/<uuid:user_id>/', UserListView.as_view()),
]