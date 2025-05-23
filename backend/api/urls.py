from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls.auth_urls')),
    path("users/view/", include('users.urls.retrieve_urls')),
    
    path("criteria/criteria-version/", include('criteria.urls.criteria_version_url')),
    path("criteria/input-type/", include('criteria.urls.input_type_url'))
]