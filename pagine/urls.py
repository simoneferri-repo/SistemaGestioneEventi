from django.urls import path

from .views import HomePageView, EventListView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("eventi", EventListView.as_view(), name="eventi"),
]
