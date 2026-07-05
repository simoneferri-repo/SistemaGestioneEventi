from django.db import IntegrityError
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from eventi_gestione.models import Eventi
from eventi_prenotazione.models import Prenotazione
from django.shortcuts import render


class PrenotazioneView(LoginRequiredMixin, View):

    def post(self, request, evento_id):
        evento = get_object_or_404(Eventi, id=evento_id)
        prenotazione_attiva_server = Prenotazione.objects.filter(utente=request.user, evento=evento).exists()

        if prenotazione_attiva_server:
            messages.warning(request, "Attenzione: hai già prenotato questo evento.")
            return HttpResponseRedirect(reverse('evento', kwargs={'pk': evento.id}))
        if evento.posti_prenotabili > 0:
            try:
                nuova_prenotazione = Prenotazione.objects.create(
                utente=request.user,
                evento=evento
                )
                evento.posti_prenotabili -= 1
                evento.save()
                messages.success(request, "<i class='bi bi-info-circle'></i> L'evento è stato prenotato correttamente!")
            except IntegrityError as e:
                print(f"Errore nel salvataggio sul Database: {e}")
                messages.error(request, "<i class='bi bi-exclamation-circle'></i> Errore durante il salvataggio della prenotazione.")
            except Exception as e:
                print(f"Errore generico: {e}")
                messages.error(request, f"Errore generico: {e}")
        else:
            messages.error(request, "Posti esauriti.")

        return HttpResponseRedirect(reverse('evento', kwargs={'pk': evento.id}))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('eventi'))

class CancellazionePrenotazioneView(LoginRequiredMixin, View):

    def post(self, request, evento_id):
        evento = get_object_or_404(Eventi, id=evento_id)
        prenotazione_attiva_server = Prenotazione.objects.filter(utente=request.user, evento=evento).exists()

        if prenotazione_attiva_server:
            try:
                elimina_prenotazione = Prenotazione.objects.filter(
                    utente=request.user,
                    evento=evento
                ).delete()
                evento.posti_prenotabili += 1
                evento.save()
                messages.success(request, "<i class='bi bi-info-circle'></i> La prenotazione è stata correttamente cancellata!")
            except IntegrityError as e:
                print(f"Errore nel salvataggio sul Database: {e}")
                messages.error(request, "<i class='bi bi-exclamation-circle'></i> Errore durante il salvataggio della prenotazione.")
            except Exception as e:
                print(f"Errore generico: {e}")
                messages.error(request, f"<i class='bi bi-exclamation-circle'></i> Errore generico: {e}")
        else:
            messages.error(request, "<i class='bi bi-exclamation-circle'></i> Non ci sono prenotazioni da cancellare.")

        return HttpResponseRedirect(reverse('evento', kwargs={'pk': evento.id}))

# Create your views here.
