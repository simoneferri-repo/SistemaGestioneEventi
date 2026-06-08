from django.contrib import admin

# Register your models here.
from .models import Eventi
admin.site.register(Eventi)

from .models import Tipologia
admin.site.register(Tipologia)