from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from eventi_gestione.models import Eventi
from django.shortcuts import render


class PrenotazioneView(LoginRequiredMixin, View):

    def post(self, request, evento_id):
        evento = get_object_or_404(Eventi, id=evento_id)

        if evento.posti_prenotabili > 0:
            evento.posti_prenotabili -= 1
            evento.save()
            messages.success(request, "L'evento è stato prenotato correttamente!")
        else:
            messages.error(request, "Posti esauriti.")

        return HttpResponseRedirect(reverse('eventi', kwargs={'evento_id': evento.id}))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('eventi'))



# Create your views here.
