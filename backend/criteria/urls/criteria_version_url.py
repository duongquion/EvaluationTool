from django.urls import path
from ..views import(
    criteria_version_view
)

urlpatterns = [
    path("",
        criteria_version_view.CriteriaVersionView.as_view(), 
        name="get-all-and-post"
    ),
    
    path("<str:version_name>/", 
        criteria_version_view.CriteriaVersionView.as_view(), 
        name="retrieve-and-patch"
    ),
]
