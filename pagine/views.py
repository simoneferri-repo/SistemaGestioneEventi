from django.views.generic import TemplateView, ListView, DetailView
from eventi_gestione.models import Eventi
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

class EventDetailView(DetailView):
    model = Eventi
    template_name = "scheda_evento.html"
    context_object_name = 'evento'