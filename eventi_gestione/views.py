from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Eventi, Tipologia
from .forms import GestioneEventiForm, GestioneTipologiaForm
from django.contrib import messages
from django.urls import reverse

# Vista che gestisce la creazione di un evento
class EventiCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Eventi
    form_class = GestioneEventiForm
    template_name = 'gestione_eventi.html'
    #success_url = reverse_lazy('eventi')

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
        messages.success(self.request, "Evento inserito con successo!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('evento', kwargs={'pk': self.object.pk})

# Vista che gestisce la modifica di un evento
class EventiUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Eventi
    form_class = GestioneEventiForm
    template_name = 'gestione_eventi.html'
    #success_url = reverse_lazy('eventi')

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
        evento = self.get_object()

        if not self.request.FILES.get('immagine_evento'):
            form.instance.immagine_evento = evento.immagine_evento

        # Impedisco la spubblicazione dell'evento se ci sono prenotazioni attive
        nuovo_stato_pubblicato = form.cleaned_data.get('pubblicato')

        if evento.pubblicato and nuovo_stato_pubblicato is False:
            if evento.prenotazione_set.exists():
                messages.error(self.request,
                           f"<i class='bi bi-exclamation-circle'></i> Impossibile spubblicare '{evento.nome_evento}': ci sono {evento.prenotazione_set.count()} prenotazioni attive. È possibile solo annullare l'evento")
                return redirect('evento', pk=evento.pk)
            else:
                messages.success(self.request, "Evento modificato con successo!")
        else:
            messages.success(self.request, "Evento modificato con successo!")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('evento', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo_pagina'] = f'Modifica: {self.object.nome_evento}'
        return context

# Vista che gestisce la cancellazione di un evento
class EventiDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Eventi
    template_name = 'conferma_elimina_evento.html'
    success_url = reverse_lazy('eventi_inseriti')

    # Solo il creatore può cancellare l'evento
    def test_func(self):
        evento = self.get_object()
        return self.request.user == evento.creatore
    def form_valid(self, form):
        evento = self.get_object()
        # Impedisco la cancellazione dell'evento se ci sono prenotazioni attive
        if evento.prenotazione_set.exists():
            messages.error(self.request, f"<i class='bi bi-exclamation-circle'></i> Impossibile cancellare '{evento.nome_evento}': ci sono {evento.prenotazione_set.count()} prenotazioni attive. È possibile solo annullare l'evento")
            return redirect('evento', pk=evento.pk)
        messages.success(self.request, "Evento eliminato con successo!")
        return super().form_valid(form)

# Vista che gestisce la creazione di una tipologia
class TipologiaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tipologia
    form_class = GestioneTipologiaForm
    template_name = 'gestione_tipologia.html'
    success_url = reverse_lazy('gestione_tipologia_creazione')

    def test_func(self):
        # Controlla se l'utente appartiene al gruppo 'redattori'
        return self.request.user.groups.filter(name='redattori').exists()

    # Faccio l'override del metodo form_valid per aggiungere in automatico l'utente creatore
    def form_valid(self, form):
        form.instance.creatore = self.request.user
        messages.success(self.request, "Tipologia inserita con successo!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipologie_esistenti'] = Tipologia.objects.all().order_by('nome_tipo')
        return context

# Vista che gestisce la modifica di una tipologia
class TipologiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tipologia
    form_class = GestioneTipologiaForm
    template_name = 'gestione_tipologia.html'
    success_url = reverse_lazy('gestione_tipologia_creazione')

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
    def form_valid(self, form):
        messages.success(self.request, "Tipologia modificata con successo!")
        return super().form_valid(form)


