from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("instance/submit", views.submit_chore_instance, name="submit_chore_instance"),
]
