from django.urls import path

from .views import HomePageView, EventListView, EventDetailView, UserEventListView, EditorEventListView, EventPrenotazioniListView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("eventi", EventListView.as_view(), name="eventi"),
    path("eventi/<int:pk>/", EventDetailView.as_view(), name="evento"),
    path("eventi_prenotati/", UserEventListView.as_view(), name="eventi_prenotati"),
    path("eventi_inseriti/", EditorEventListView.as_view(), name="eventi_inseriti"),
    path('eventi/<int:evento_id>/prenotazioni/', EventPrenotazioniListView.as_view(), name='evento_prenotazioni'),
]
