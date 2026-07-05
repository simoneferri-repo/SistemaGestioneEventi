from django.contrib import admin

# Register your models here.
from .models import Eventi
# admin.site.register(Eventi)

# Definisco la tabella con i campi da visualizzare in admin usando il decoratore @admin.register. Metto anche le prenotazioni attive
@admin.register(Eventi)
class EventiAdmin(admin.ModelAdmin):
    list_display = ('nome_evento', 'luogo_evento', 'data_semplice', 'tipo_evento', 'posti_prenotabili', 'prenotazioni_attive', 'pubblicato', 'annullato')
    sortable_by = ('nome_evento', 'luogo_evento', 'data_semplice', 'tipo_evento', 'posti_prenotabili', 'pubblicato', 'annullato')

    # Definisco come visulizzare la data/orario usando il decoratore @admin.display
    @admin.display(description='Data Evento', ordering='data_ora_evento')
    def data_semplice(self, obj):
        if obj.data_ora_evento:
            return obj.data_ora_evento.strftime('%d/%m/%Y %H:%M')
        return "-"

    # Vado a conteggiare le prenotazioni di ogni evento sfruttando la relazione inversa "prenotazione_set"
    @admin.display(description='Prenotazioni')
    def prenotazioni_attive(self, obj):
        return obj.prenotazione_set.count()


from .models import Tipologia

@admin.register(Tipologia)
class TipologiaAdmin(admin.ModelAdmin):
    list_display = ('nome_tipo', 'n_eventi')
    sortable_by = ('nome_tipo')

    @admin.display(description='Eventi')
    def n_eventi(self, obj):
        return obj.eventi_set.count()