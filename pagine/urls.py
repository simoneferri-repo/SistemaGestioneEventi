from django.urls import path

from .views import HomePageView, EventListView, EventDetailView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("eventi", EventListView.as_view(), name="eventi"),
    path("eventi/<int:pk>/", EventDetailView.as_view(), name="evento"),
]
