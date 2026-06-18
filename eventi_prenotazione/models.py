from django.db import models
from eventi_gestione.models import Eventi
from eventi_accounts.models import CustomUser

class Prenotazione(models.Model):
    STATI_PRENOTAZIONE = [
        ('ATTIVA', 'Attiva'),
        ('CANCELLATA', 'Cancellata'),
    ]
    utente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventi, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField(auto_now_add=True)
    stato = models.CharField(max_length=20, choices=STATI_PRENOTAZIONE, default='ATTIVA')

    class Meta:
        unique_together = ('utente', 'evento')

    def __str__(self):
        return f"{self.utente.username} - {self.evento.nome_evento} ({self.data_prenotazione.strftime('%d/%m/%Y')})"