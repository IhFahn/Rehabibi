from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("setup/", views.setup, name="setup"),
    path("detection/", views.detection, name="detection"),
    path("home_dev/", views.home_dev, name="home_dev"),
    path("setup_dev/", views.setup_dev, name="setup_dev"),
    path("setup_dev/durrep_dev/", views.durrep_dev, name="durrep_dev"),
    path("detection_dev/", views.detection_dev, name="detection_dev"),
    #path("video_feed/", views.video_feed, name="video_feed"),
    path("webcam_feed/", views.webcam_feed, name="webcam_feed"),

]