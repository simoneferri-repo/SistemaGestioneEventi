from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        nuovo_utente = self.object
        gruppo_visitatori, created = Group.objects.get_or_create(name='visitatori')
        nuovo_utente.groups.add(gruppo_visitatori)
        return response