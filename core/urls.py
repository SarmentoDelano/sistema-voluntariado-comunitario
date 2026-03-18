from django.urls import path
from .views import acoes_list, campanhas, minhas_inscricoes

urlpatterns = [
    path('acoes/', acoes_list, name='acoes_list'),
    path('campanhas/', campanhas, name='campanhas'),
    path('minhas-inscricoes/', minhas_inscricoes, name='minhas_inscricoes'),
]