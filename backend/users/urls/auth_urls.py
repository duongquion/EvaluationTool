from django.urls import path
from users.views import auth_views as auth

urlpatterns = [
    path('change-password/', auth.change_password, name="change-password"),
    path("set-init-password/", auth.set_password, name="set-init-password"),
    path("login/", auth.login, name="login"),
]