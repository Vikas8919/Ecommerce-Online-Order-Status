from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/',views.profile_view,name="profile"),
    path('intro/', views.intro_view, name='intro'),
]