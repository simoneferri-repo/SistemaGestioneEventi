from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Eventi, Tipologia
from .forms import GestioneEventiForm, GestioneTipologiaForm

class EventiCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Eventi
    form_class = GestioneEventiForm
    template_name = 'gestione_eventi.html'
    success_url = reverse_lazy('eventi')

    def test_func(self):
        # Controlla se l'utente appartiene al gruppo 'editor'
        return self.request.user.groups.filter(name='redattori').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo_pagina'] = 'Nuovo Evento'
        return context
    # Faccio l'override del metodo form_valid per aggiungere in automatico l'utente creatore
    def form_valid(self, form):

        form.instance.creatore = self.request.user
        return super().form_valid(form)

class EventiUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Eventi
    form_class = GestioneEventiForm
    template_name = 'gestione_eventi.html'
    success_url = reverse_lazy('eventi')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        evento = self.get_object()

        # Controlla se l'utente è l'utente creatore
        return self.request.user == evento.creatore
        # return self.request.user.groups.filter(name='redattori').exists()

    def form_valid(self, form):
        if not self.request.FILES.get('immagine_evento'):
            form.instance.immagine_evento = self.get_object().immagine_evento
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo_pagina'] = f'Modifica: {self.object.nome_evento}'
        return context

class EventiDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Eventi
    template_name = 'conferma_elimina_evento.html'
    success_url = reverse_lazy('eventi_inseriti')

    # Solo il creatore può cancellare l'evento
    def test_func(self):
        evento = self.get_object()
        return self.request.user == evento.creatore

class TipologiaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tipologia
    form_class = GestioneTipologiaForm
    template_name = 'gestione_tipologia.html'
    success_url = reverse_lazy('tipologie')

    def test_func(self):
        # Controlla se l'utente appartiene al gruppo 'editor'
        return self.request.user.groups.filter(name='redattori').exists()

    # Faccio l'override del metodo form_valid per aggiungere in automatico l'utente creatore
    def form_valid(self, form):
        form.instance.creatore = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipologie_esistenti'] = Tipologia.objects.all().order_by('nome_tipo')
        return context

class TipologiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tipologia
    form_class = GestioneTipologiaForm
    template_name = 'gestione_tipologia.html'
    success_url = reverse_lazy('tipologie')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        tipologia = self.get_object()
        return self.request.user == tipologia.creatore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo_pagina'] = f'Modifica: {self.object.nome_tipo}'
        return context



