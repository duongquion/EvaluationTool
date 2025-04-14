from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls.auth_urls')),
    path("users/view/", include('users.urls.retrieve_urls')),
    path("criteria/", include('criteria.urls'))
]