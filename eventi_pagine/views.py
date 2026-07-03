from django.views.generic import TemplateView, ListView, DetailView
from eventi_gestione.models import Eventi
from django.contrib.auth.mixins import LoginRequiredMixin
from eventi_prenotazione.models import Prenotazione
from django.contrib import messages
from django.utils import timezone


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        context['eventi_prossimi'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale).order_by('data_ora_evento')[:6]

        if self.request.user.is_authenticated:

            prenotazioni_annullate = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=True
            )
            context['prenotazioni_attive'] = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=False
            ).order_by('evento__data_ora_evento')[:3]
            context['eventi_prenotati_ids'] = set(
                Prenotazione.objects.filter(utente=self.request.user).values_list('evento_id', flat=True)
            )

            if prenotazioni_annullate.exists():
                testo_msg_annullato = "<i class='fs-4 bi bi-exclamation-triangle'></i> Uno o più eventi a cui eri prenotato sono stati annullati <i class='fs-4 bi bi-exclamation-triangle'></i> <ul>"

                for prenotazione in prenotazioni_annullate:
                    testo_msg_annullato += f"<li><a href='/eventi/{prenotazione.evento.id}/'>{prenotazione.evento.nome_evento} del {prenotazione.evento.data_ora_evento.strftime('%d/%m/%Y ore %H:%M')}</a></li>"

                testo_msg_annullato += "</ul><p>Per far sparire questo avviso è necessario annullare manualmente la prenotazione.</p>"

                messages.error(self.request,testo_msg_annullato)

        return context

class EventListView(ListView):
    model = Eventi
    template_name = "lista_eventi.html"
    context_object_name = 'eventi'


    def get_context_data(self, **kwargs):
        ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        context['eventi_futuri'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale).order_by('data_ora_evento')

        if self.request.user.is_authenticated:
            context['eventi_prenotati_ids'] = set(
                Prenotazione.objects.filter(utente=self.request.user).values_list('evento_id', flat=True)
            )

        return context
class UserEventListView(LoginRequiredMixin,ListView):
    model = Prenotazione
    template_name = "prenotazioni_utente.html"
    context_object_name = 'prenotazioni_utente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            prenotazioni_annullate = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=True
            )

            if prenotazioni_annullate.exists():
                testo_msg_annullato = "<i class='fs-4 bi bi-exclamation-triangle'></i> Uno o più eventi a cui eri prenotato sono stati annullati <i class='fs-4 bi bi-exclamation-triangle'></i> <ul>"

                for prenotazione in prenotazioni_annullate:
                    testo_msg_annullato += f"<li><a href='/eventi/{prenotazione.evento.id}/'>{prenotazione.evento.nome_evento} del {prenotazione.evento.data_ora_evento.strftime('%d/%m/%Y ore %H:%M')}</a></li>"

                testo_msg_annullato += "</ul><p>Per far sparire questo avviso è necessario annullare manualmente la prenotazione.</p>"

                messages.error(self.request,testo_msg_annullato)

        return context

    def get_queryset(self):
        return Prenotazione.objects.filter(utente=self.request.user).select_related('evento').order_by('evento__data_ora_evento')

class EventDetailView(DetailView):
    model = Eventi
    template_name = "scheda_evento.html"
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        #global prenotazione_on
        context = super().get_context_data(**kwargs)
        prenotazione_on = False
        if self.request.user.is_authenticated:
            prenotazione_on = Prenotazione.objects.filter(
                utente=self.request.user,
                evento=self.get_object()
            ).exists()
        context['prenotazione_attiva'] = prenotazione_on

        evento = self.object
        context['is_creatore'] = self.request.user == evento.creatore

        return context

class EditorEventListView(LoginRequiredMixin, ListView):
    model = Eventi
    template_name = 'gestione_eventi_elenco.html'
    context_object_name = 'gestione_eventi_elenco'

    def get_queryset(self):
        return Eventi.objects.filter(creatore=self.request.user)