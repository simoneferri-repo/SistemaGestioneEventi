from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# viene ridefinito il form standard per gestire anche i campi personalizzati del modello CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'eta', 'telefono')