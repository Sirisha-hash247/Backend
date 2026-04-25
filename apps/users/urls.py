from django.urls import path
from .views import RegisterView, LoginView, UserListView

urlpatterns = [
    #  AUTH
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('manage/', UserListView.as_view()),                 # GET, POST
    path('manage/<uuid:user_id>/', UserListView.as_view()),  # PATCH, DELETE
]