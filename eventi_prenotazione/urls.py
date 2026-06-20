from django.urls import path
from .views import PrenotazioneView, CancellazioneView

urlpatterns = [
    path('eventi/<int:evento_id>/prenota', PrenotazioneView.as_view(), name='prenota_evento'),
    path('eventi/<int:evento_id>/cancella', CancellazioneView.as_view(), name='cancella_evento'),
]