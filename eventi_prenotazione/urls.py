from django.urls import path
from .views import PrenotazioneView, CancellazionePrenotazioneView

urlpatterns = [
    path('eventi/<int:evento_id>/prenota/', PrenotazioneView.as_view(), name='prenota_evento'),
    path('eventi/<int:prenotazione_id>/cancella/', CancellazionePrenotazioneView.as_view(), name='cancella_prenotazione_evento'),
]