from django import forms
from django.forms import ModelForm
from .models import Eventi, Tipologia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML

class GestioneEventiForm(ModelForm):
    data_ora_evento = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            },
            format='%Y-%m-%dT%H:%M'
        ),
        label="Data e ora dell'evento"
    )

    class Meta:
        model = Eventi
        fields = ['nome_evento', 'descrizione_evento', 'tipo_evento', 'luogo_evento', 'data_ora_evento', 'immagine_evento', 'prezzo', 'posti_prenotabili', 'annullato', 'pubblicato']
        labels = {
            'immagine_evento': 'Immagine evento (dimensioni 500px x 350px)',
        }

# Verifico che venga selezionato almeno una tipologia per l'evento
    def clean_tipo_evento(self):
        tipologie = self.cleaned_data.get('tipo_evento')

        if not tipologie:
            raise forms.ValidationError("Devi selezionare almeno una tipologia per l'evento.")

        return tipologie

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Visualizzo il nome del creatore in modifica dell'evento
        if self.instance and self.instance.pk and getattr(self.instance, 'creatore', None):
            creatore_html = HTML(f'''
                        <div class="mb-3">
                            <div class="form-control-plaintext text-muted">Evento creato da: <strong>{self.instance.creatore.username}</strong></div>
                        </div>
                    ''')
        else:
            creatore_html = HTML('''
                            <div class="alert alert-info py-2 mb-3">
                                <i class="bi bi-info-circle"></i> L'evento verrà registrato a tuo nome.
                            </div>
                        ''')

        if hasattr(self.instance, 'data_ora_evento') and self.instance.data_ora_evento:
            self.initial['data_ora_evento'] = self.instance.data_ora_evento.strftime('%Y-%m-%d %H:%M')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            Column(creatore_html, css_class='col-md-4'),
            Row(
                Column(Field('tipo_evento'), css_class='col-md-6'),
            ),
            Field('nome_evento', placeholder='Titolo evento'),
            Field('descrizione_evento', rows=4),

            Row(
                Column(Field('luogo_evento', placeholder='Luogo dell\'evento'), css_class='col-md-6'),
                Column(Field('data_ora_evento'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('immagine_evento'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('prezzo', placeholder='Prezzo'), css_class='col-md-2'),
                Column(Field('posti_prenotabili', placeholder='N. posti prenotabili'), css_class='col-md-3'),
            ),
            Row(
                Column(Field('annullato', placeholder='Evento annullato'), css_class='col-md-3'),
                Column(Field('pubblicato', placeholder='Evento pubblicato'), css_class='col-md-3'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary mt-2'),
        )
class GestioneTipologiaForm(ModelForm):
    class Meta:
        model = Tipologia
        fields = ['nome_tipo']
        #fields = '--__all__'
        labels = {
            'nome_tipo': 'Nome',
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Visualizzo il nome del creatore in modifica della tipologia
        if self.instance and self.instance.pk and getattr(self.instance, 'creatore', None):
            creatore_html = HTML(f'''
                        <div class="mb-3">
                            <div class="form-control-plaintext text-muted">Tipologia creata da: <strong>{self.instance.creatore.username}</strong></div>
                        </div>
                    ''')
        else:
            creatore_html = HTML('''
                            <div class="alert alert-info py-2 mb-3">
                                <i class="bi bi-info-circle"></i> La tipologia verrà registrato a tuo nome.
                            </div>
                        ''')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Column(creatore_html, css_class='col-md-6'),
            Column( Field('nome_tipo', placeholder='Nome tipologia'), css_class='col-md-6'),
            Submit('submit', 'Salva', css_class='btn btn-primary mt-2'),
        )

# controllo che venga selezionato lamno una tipologia per l'evento
class EventiAdminForm(forms.ModelForm):
    class Meta:
        model = Eventi
        fields = '__all__'

    def clean_tipo_evento(self):
        tipologie = self.cleaned_data.get('tipo_evento')
        if not tipologie or tipologie.count() == 0:
            raise forms.ValidationError("Attenzione: seleziona almeno una tipologia.")
        return tipologie