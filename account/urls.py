from django.urls import path
from rest_framework import permissions
from account.views import RegistrationView, ActivationView, LoginView, UserListView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('register_phone/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', UserListView.as_view())
]

