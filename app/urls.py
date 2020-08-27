from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("worm/review", views.worm_review, name="worm_review"),
    path("worm/review/submit", views.submit_worm_verdict, name="submit_worm_verdict"),
    path("instance/submit", views.submit_chore_instance, name="submit_chore_instance"),
    # Detail page
    # path("instance/<int:pk>", )),
    # New submission link
    # path("instance/<int:pk>/submit", )),
]
