from django.db import models
from eventi_accounts.models import CustomUser

# Create your models here.

class Tipologia(models.Model):
    nome_tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_tipo

class Eventi(models.Model):
    nome_evento = models.CharField(max_length=100)
    descrizione_evento = models.TextField()
    tipo_evento = models.ForeignKey(Tipologia,on_delete=models.CASCADE)
    luogo_evento = models.CharField(max_length=100)
    data_ora_evento = models.DateTimeField()
    immagine_evento = models.ImageField(upload_to='eventi/', blank=True, null=True)
    posti_prenotabili = models.PositiveIntegerField(null=True, blank=True)
    creatore = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='eventi_creati')

    def __str__(self):
       # return self.nome_evento
        data_semplice = self.data_ora_evento.strftime('%d/%m/%Y %H:%M')
        return f"{self.nome_evento} - {self.luogo_evento} - {data_semplice} ({self.tipo_evento})"