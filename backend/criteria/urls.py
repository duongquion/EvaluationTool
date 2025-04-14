from django.urls import path
from .views import(
    criteria_version_views
)

urlpatterns = [
    path("criteria-version/",
        criteria_version_views.CriteriaVersionView.as_view(), 
        name="criteria-version-get-all-and-post"
    ),
    
    path("criteria-version/<str:version_name>/", 
        criteria_version_views.CriteriaVersionView.as_view(), 
        name="criteria-version-retrieve-and-patch"
    ),
]
