from django.views.generic import TemplateView, ListView, DetailView
from eventi_gestione.models import Eventi
from django.contrib.auth.mixins import LoginRequiredMixin
from eventi_prenotazione.models import Prenotazione
from django.utils import timezone


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        context['eventi_prossimi'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale).order_by('data_ora_evento')[:6]

        return context

class EventListView(ListView):
    model = Eventi
    template_name = "lista_eventi.html"
    context_object_name = 'eventi'

    def get_context_data(self, **kwargs):
        ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        context['eventi_futuri'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale).order_by('data_ora_evento')

        return context
class UserEventListView(LoginRequiredMixin,ListView):
    model = Prenotazione
    template_name = "prenotazioni_utente.html"
    context_object_name = 'prenotazioni_utente'

    def get_queryset(self):
        return Prenotazione.objects.filter(utente=self.request.user).select_related('evento').order_by('-data_prenotazione')

class EventDetailView(DetailView):
    model = Eventi
    template_name = "scheda_evento.html"
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        #global prenotazione_on
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            prenotazione_on = Prenotazione.objects.filter(
                utente=self.request.user,
                evento=self.get_object()
            ).exists()
        context['prenotazione_attiva'] = prenotazione_on

        return context