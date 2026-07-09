from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import CustomUser

# Vista che gestisce l'iscrizione dell'utente
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        nuovo_utente = self.object
        gruppo_visitatori, created = Group.objects.get_or_create(name='visitatori')
        nuovo_utente.groups.add(gruppo_visitatori)
        messages.success(self.request, "Iscrizione effettuata con successo!!")
        return response

User = get_user_model()

# Vista che gestisce la modifica di un utente
class EditUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'edit_profilo.html'
    success_url = reverse_lazy('modifica_profilo')

    fields = ['username', 'first_name', 'last_name', 'email', 'eta', 'telefono']
    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Dati modificati con successo!!")
        return super().form_valid(form)