from django.urls import path
from .views import UserListCreateAPIView, UserDetailAPIView, UserChangePasswordView

urlpatterns = [
    path('users/',UserListCreateAPIView.as_view(), name='users'),
    path('users/<int:pk>/',UserDetailAPIView.as_view(), name='users'),
    path('users/change-password/',UserChangePasswordView.as_view(), name='change_password'),
]
