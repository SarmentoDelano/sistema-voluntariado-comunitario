from django.contrib import admin
from .models import Voluntario, AcaoComunitaria, Inscricao, Campanha

admin.site.register(Voluntario)
admin.site.register(AcaoComunitaria)
admin.site.register(Inscricao)
admin.site.register(Campanha)