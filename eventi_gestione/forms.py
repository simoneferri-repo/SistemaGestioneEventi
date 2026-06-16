from django import forms
from django.forms import ModelForm
from .models import Eventi
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

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
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
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