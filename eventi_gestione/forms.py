from django import forms
from django.forms import ModelForm
from .models import Eventi, Tipologia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML

class GestioneEventiForm(ModelForm):
    data_ora_evento = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={'placeholder': 'gg/mm/aaaa hh:mm'}
        )
    )
    class Meta:
        model = Eventi
        fields = ['nome_evento', 'descrizione_evento', 'tipo_evento', 'luogo_evento', 'data_ora_evento', 'immagine_evento', 'posti_prenotabili']
        #fields = '--__all__'

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

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

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            Column(creatore_html, css_class='col-md-4'),
            Field('nome_evento', placeholder='Titolo evento'),
            Field('descrizione_evento', rows=4),
            Row(
                Column(Field('tipo_evento'), css_class='col-md-6'),
                Column(Field('luogo_evento', placeholder='Luogo dell\'evento'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('data_ora_evento'), css_class='col-md-6'),
                Column(Field('immagine_evento'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('posti_prenotabili', placeholder='N. posti prenotabili'), css_class='col-md-3'),
            ),
            Submit('submit', 'Salva', css_class='btn btn-primary mt-2'),
        )
class GestioneTipologiaForm(ModelForm):
    class Meta:
        model = Tipologia
        fields = ['nome_tipo']
        #fields = '--__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('nome_tipo', placeholder='Nome tipologia'),
            Submit('submit', 'Salva', css_class='btn btn-primary mt-2'),
        )