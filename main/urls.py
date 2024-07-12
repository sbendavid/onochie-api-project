# urls.py
from django.urls import path
from .views import MyTokenObtainPairView, register, get_user, create_organisation, get_organisations

urlpatterns = [
    path('auth/register', register),
    path('auth/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/<int:id>', get_user, name='get_user'),
    path('organisation', create_organisation, name='create_organisation'),
    path('organisations', get_organisations, name='get_organisation'),
]
