from django.urls import path
from .views import PrenotazioneView

urlpatterns = [
    path('eventi/<int:evento_id>/prenota', PrenotazioneView.as_view(), name='prenota_evento'),
]