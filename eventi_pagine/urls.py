from django.urls import path

from .views import HomePageView, EventListView, EventDetailView, UserEventListView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("eventi", EventListView.as_view(), name="eventi"),
    path("eventi/<int:pk>/", EventDetailView.as_view(), name="evento"),
    path("eventi_prenotati/", UserEventListView.as_view(), name="eventi_prenotati"),
]
