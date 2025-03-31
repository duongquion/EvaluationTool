from django.urls import path
from users.views import retrieve_views as user
urlpatterns = [
    path("list-team/", user.list_team, name="list-team"),
]