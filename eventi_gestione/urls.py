from django.urls import path

from .views import EventiCreateView, EventiUpdateView, EventiDeleteView, TipologiaCreateView, TipologiaUpdateView

urlpatterns = [
    path("gestione_eventi/", EventiCreateView.as_view(), name="gestione_eventi_creazione"),
    path("gestione_eventi/<int:pk>/", EventiUpdateView.as_view(), name="gestione_eventi_modifica"),
    path('gestione_eventi/<int:pk>/elimina/', EventiDeleteView.as_view(), name='gestione_eventi_elimina'),
    path("gestione_tipologia/", TipologiaCreateView.as_view(), name="gestione_tipologia_creazione"),
    path("gestione_tipologia/<int:pk>/", TipologiaUpdateView.as_view(), name="gestione_tipologia_modifica"),
]