from django.urls import path
from . import views

urlpatterns = [
    path("upload_excel/", views.excel_upload, name="excel_upload"),
    path("upload_excel/confirm/", views.excel_confirm, name="excel_confirm"),
]