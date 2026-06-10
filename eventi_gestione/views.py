from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Eventi
from .forms import GestioneEventiForm

class EventiCreateView(CreateView):
    model = Eventi
    form_class = GestioneEventiForm
    template_name = 'gestione_eventi.html'
    success_url = reverse_lazy('eventi')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo_pagina'] = 'Nuovo Evento'
        return context
class EventiUpdateView(UpdateView):
    model = Eventi
    form_class = GestioneEventiForm
    template_name = 'gestione_eventi.html'
    success_url = reverse_lazy('eventi')

    def form_valid(self, form):
        if not self.request.FILES.get('immagine_evento'):
            form.instance.immagine_evento = self.get_object().immagine_evento
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo_pagina'] = f'Modifica: {self.object.nome_evento}'
        return context