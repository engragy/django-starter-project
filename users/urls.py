from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('user/set-pass/', views.CustomUserSetPassword.as_view()),
    path('user/status/', views.CustomUserSetStatus.as_view()),
]
