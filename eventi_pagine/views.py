from django.views.generic import TemplateView, ListView, DetailView
from eventi_gestione.models import Eventi, Tipologia
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from eventi_prenotazione.models import Prenotazione
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404

# Vista che gestisce la home page
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        context['eventi_prossimi'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale, pubblicato=True).order_by('data_ora_evento')[:6]



        if self.request.user.is_authenticated:
            # Verifico se esistono prenotazioni annullate
            prenotazioni_annullate = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=True,
                evento__data_ora_evento__gte=timezone.now()
            )
            # Estraggo le prossime 4 prenotazioni dell'utente
            context['prenotazioni_attive'] = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=False
            ).order_by('evento__data_ora_evento')[:4]
            context['eventi_prenotati_ids'] = set(
                Prenotazione.objects.filter(utente=self.request.user).values_list('evento_id', flat=True)
            )

            # Visualizzo un messaggio se ci sono prenotazioni attive su eventi annullati
            if prenotazioni_annullate.exists():
                testo_msg_annullato = "<i class='fs-4 bi bi-exclamation-triangle'></i> Uno o più eventi a cui eri prenotato sono stati annullati <i class='fs-4 bi bi-exclamation-triangle'></i> <ul>"

                for prenotazione in prenotazioni_annullate:
                    testo_msg_annullato += f"<li><a href='/eventi/{prenotazione.evento.id}/'>{prenotazione.evento.nome_evento} del {prenotazione.evento.data_ora_evento.strftime('%d/%m/%Y ore %H:%M')}</a></li>"

                testo_msg_annullato += "</ul><p>Per far sparire questo avviso è necessario annullare manualmente la prenotazione.</p>"

                messages.error(self.request,testo_msg_annullato)

        return context

# Vista che gestisce l'elenco degli eventi
class EventListView(ListView):
    model = Eventi
    template_name = "lista_eventi.html"
    context_object_name = 'eventi_futuri'
    paginate_by = 9

    def get_queryset(self):
        ora_attuale = timezone.now()
        queryset = Eventi.objects.filter(
            data_ora_evento__gte=ora_attuale,
            pubblicato=True
        ).order_by('data_ora_evento')

        # Gestisco i filtri per tipologia
        tipologia_id = self.request.GET.get('tipologia')

        if tipologia_id:
            queryset = queryset.filter(tipo_evento__id=tipologia_id).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        #ora_attuale = timezone.now()
        context = super().get_context_data(**kwargs)
        #context['eventi_futuri'] = Eventi.objects.filter(data_ora_evento__gte=ora_attuale, pubblicato=True).order_by('data_ora_evento')

        if self.request.user.is_authenticated:
            context['eventi_prenotati_ids'] = set(
                Prenotazione.objects.filter(utente=self.request.user).values_list('evento_id', flat=True)
            )

        # Gestisco i filtri per tipologia
        context['tipologie'] = Tipologia.objects.all()
        context['tipologia_selezionata'] = self.request.GET.get('tipologia')

        if context['tipologia_selezionata']:
            try:
                context['tipologia_corrente'] = Tipologia.objects.get(id=context['tipologia_selezionata'])
            except Tipologia.DoesNotExist:
                context['tipologia_corrente'] = None

        return context

# Vista che gestisce l'elenco degli eventi prenotati dall'utente
class UserEventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Prenotazione
    template_name = "prenotazioni_utente.html"
    context_object_name = 'prenotazioni_utente'

    def test_func(self):
        # Controlla se l'utente appartiene al gruppo 'visitatori'
        return self.request.user.groups.filter(name='visitatori').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            prenotazioni_annullate = Prenotazione.objects.filter(
                utente=self.request.user,
                evento__annullato=True,
                evento__data_ora_evento__gte = timezone.now()
            )
            # Faccio apparire un messaggio se ci sono prenotazioni attive su eventi annullati
            if prenotazioni_annullate.exists():
                testo_msg_annullato = "<i class='fs-4 bi bi-exclamation-triangle'></i> Uno o più eventi a cui eri prenotato sono stati annullati <i class='fs-4 bi bi-exclamation-triangle'></i> <ul>"

                for prenotazione in prenotazioni_annullate:
                    testo_msg_annullato += f"<li><a href='/eventi/{prenotazione.evento.id}/'>{prenotazione.evento.nome_evento} del {prenotazione.evento.data_ora_evento.strftime('%d/%m/%Y ore %H:%M')}</a></li>"

                testo_msg_annullato += "</ul><p>Per far sparire questo avviso è necessario annullare manualmente la prenotazione.</p>"

                messages.error(self.request,testo_msg_annullato)

        # Contesto per visualizzare le prenotazioni passate
        context['prenotazioni_passate'] = Prenotazione.objects.filter(utente=self.request.user,evento__data_ora_evento__lt = timezone.now()).select_related('evento').order_by('-evento__data_ora_evento')

        return context

    def get_queryset(self):
        return Prenotazione.objects.filter(utente=self.request.user, evento__data_ora_evento__gte=timezone.now()).select_related('evento').order_by('evento__data_ora_evento')

# Vista che gestisce la pagina di dettaglio dell'evento
class EventDetailView(DetailView):
    model = Eventi
    template_name = "scheda_evento.html"
    context_object_name = 'evento'

    def render_to_response(self, context, **response_kwargs):
        evento = self.object

        # Faccio apparire un avviso e rendo un codice http 404 se l'evento è scaduto
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

    # Definisco il contesto per intercettare se l'evento è già prenotato e se l'utente è il creatore
    def get_context_data(self, **kwargs):
        #global prenotazione_on
        context = super().get_context_data(**kwargs)
        prenotazione_on = False
        prenotazione_fatta = None
        if self.request.user.is_authenticated:
            prenotazione_on = Prenotazione.objects.filter(
                utente=self.request.user,
                evento=self.get_object()
            ).exists()
            if prenotazione_on:
                prenotazione_fatta = Prenotazione.objects.filter(
                    utente=self.request.user,
                    evento=self.get_object()
                ).first().id
        context['prenotazione_attiva'] = prenotazione_on
        context['prenotazione_identificativo'] = prenotazione_fatta
        evento = self.object
        context['is_creatore'] = self.request.user == evento.creatore

        return context

# Vista che gestisce l'elenco degli eventi inseriti dal redattore
class EditorEventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Eventi
    template_name = 'gestione_eventi_elenco.html'
    context_object_name = 'gestione_eventi_elenco'

    def get_queryset(self):
        return Eventi.objects.filter(creatore=self.request.user, data_ora_evento__gte = timezone.now()).order_by('data_ora_evento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Contesto per visualizzare gli eventi inseriti passati
        context['eventi_inseriti_passati'] = Eventi.objects.filter(creatore=self.request.user,data_ora_evento__lt = timezone.now()).order_by('data_ora_evento')

        return context

    def test_func(self):
        # Controlla se l'utente appartiene al gruppo 'redattori'
        return self.request.user.groups.filter(name='redattori').exists()

# Vista che gestisce l'elenco delle prenotazioni di un evento
class EventPrenotazioniListView(UserPassesTestMixin, ListView):
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

    def test_func(self):
        # Controlla se l'utente appartiene al gruppo 'redattori'
        return self.request.user.groups.filter(name='redattori').exists()