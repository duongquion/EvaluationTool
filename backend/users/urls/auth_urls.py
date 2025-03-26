from django.urls import path
from users.views import auth_views as auth
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('change-password/', auth.change_password, name="change-password"),
    path("set-init-password/", auth.set_password, name="set-init-password"),
    path("login/", auth.login, name="login"),
    path("get-question/<str:username>/", auth.get_question, name="get-question"),
    path("forgot-password/", auth.forgot_password, name="forgot-password"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token")
]