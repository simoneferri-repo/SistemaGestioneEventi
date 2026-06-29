from django.urls import path

from .views import EventiCreateView, EventiUpdateView, TipologiaCreateView

urlpatterns = [
    path("gestione_eventi/", EventiCreateView.as_view(), name="gestione_eventi_creazione"),
    path("gestione_eventi/<int:pk>/", EventiUpdateView.as_view(), name="gestione_eventi_modifica"),
    path("gestione_tipologia/", TipologiaCreateView.as_view(), name="gestione_eventi_creazione"),
]