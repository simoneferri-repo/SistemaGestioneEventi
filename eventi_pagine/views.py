from django.views.generic import TemplateView, ListView, DetailView
from eventi_gestione.models import Eventi
from django.contrib.auth.mixins import LoginRequiredMixin
from eventi_prenotazione.models import Prenotazione, Eventi
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        context['eventi_prossimi'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale, pubblicato=True).order_by('data_ora_evento')[:6]



        if self.request.user.is_authenticated:

            prenotazioni_annullate = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=True,
                evento__data_ora_evento__gte=timezone.now()
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
        context['eventi_futuri'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale, pubblicato=True).order_by('data_ora_evento')

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
                evento__annullato=True,
                evento__data_ora_evento__gte = timezone.now()
            )

            if prenotazioni_annullate.exists():
                testo_msg_annullato = "<i class='fs-4 bi bi-exclamation-triangle'></i> Uno o più eventi a cui eri prenotato sono stati annullati <i class='fs-4 bi bi-exclamation-triangle'></i> <ul>"

                for prenotazione in prenotazioni_annullate:
                    testo_msg_annullato += f"<li><a href='/eventi/{prenotazione.evento.id}/'>{prenotazione.evento.nome_evento} del {prenotazione.evento.data_ora_evento.strftime('%d/%m/%Y ore %H:%M')}</a></li>"

                testo_msg_annullato += "</ul><p>Per far sparire questo avviso è necessario annullare manualmente la prenotazione.</p>"

                messages.error(self.request,testo_msg_annullato)

        context['prenotazioni_passate'] = Prenotazione.objects.filter(utente=self.request.user,evento__data_ora_evento__lt = timezone.now()).select_related('evento').order_by('-evento__data_ora_evento')

        return context

    def get_queryset(self):
        return Prenotazione.objects.filter(utente=self.request.user, evento__data_ora_evento__gte=timezone.now()).select_related('evento').order_by('evento__data_ora_evento')

class EventDetailView(DetailView):
    model = Eventi
    template_name = "scheda_evento.html"
    context_object_name = 'evento'

    def render_to_response(self, context, **response_kwargs):
        evento = self.object

        if evento.data_ora_evento < timezone.now():
            response_kwargs['status'] = 404
            messages.error(self.request,
                       f"<i class='bi bi-exclamation-triangle'></i> Attenzione! L'evento che stai guardando è già passato.! La scheda viene mantenuta solo per motivi di archivio.")

        return super().render_to_response(context, **response_kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not obj.pubblicato:
            is_redattore = self.request.user.groups.filter(name='redattori').exists()
            if not is_redattore:
                raise Http404("Evento non pubblicato")

        return obj
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
        return Eventi.objects.filter(creatore=self.request.user, data_ora_evento__gte = timezone.now()).order_by('data_ora_evento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['eventi_inseriti_passati'] = Eventi.objects.filter(creatore=self.request.user,data_ora_evento__lt = timezone.now()).order_by('data_ora_evento')

        return context

class EventPrenotazioniListView(ListView):
    model = Prenotazione
    template_name = 'prenotazioni_evento.html'
    context_object_name = 'prenotazioni'

    def get_queryset(self):
        self.evento = get_object_or_404(Eventi, pk=self.kwargs['evento_id'])
        return Prenotazione.objects.filter(evento=self.evento).order_by('data_prenotazione')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = self.evento
        return context