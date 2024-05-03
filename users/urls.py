from django.urls import path
from .views import AddressView, ChangePasswordView, CustomLogoutView, RegisterAndLoginView, ProfileView

urlpatterns = [
    path(
        'login-register/',
        RegisterAndLoginView.as_view(),
        name='login_register'
    ),
    path(
        'profile/',
        ProfileView.as_view(),
        name='profile'
    ),
    path(
        'change_password/',
        ChangePasswordView.as_view(),
        name='change_password'
    ),
    path(
        'address/',
        AddressView.as_view(),
        name='address'
    ),
    path(
        'logout/',
        CustomLogoutView.as_view(),
        name='logout'
    )
]
