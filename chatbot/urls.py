
from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.upload_pdf,
        name="upload_pdf"
    ),

    path(
        "extract/<int:pk>/",
        views.extract_pdf,
        name="extract_pdf"
    ),

    path(
        "search/",
        views.search_pdf,
        name="search_pdf"
    ),

]
