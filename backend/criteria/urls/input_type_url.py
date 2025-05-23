from django.urls import path
from ..views import input_type_view

urlpatterns = [
    path("", 
        input_type_view.InputTypeView.as_view(),
        name="get-all-and-post"
    ),
    path("<int:id>/",
        input_type_view.InputTypeView.as_view(),
        name="retrieve-and-patch"
    )
]
