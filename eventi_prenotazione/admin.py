from django.contrib import admin


# Register your models here.
from .models import Prenotazione


@admin.register(Prenotazione)
class PrenotazioniAdmin(admin.ModelAdmin):
    list_display = ('utente', 'evento', 'data_prenotazione')
    sortable_by = ('utente', 'evento', 'data_prenotazione')

    list_filter = (
        'utente',
        'data_prenotazione',
        'evento',
    )
