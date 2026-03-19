from django.urls import path
from .views import (
    acoes_list,
    campanhas,
    minhas_inscricoes,
    cadastro_voluntario_view,
    acao_create,
    acao_update,
    inscrever_acao,
    inscritos_acao,
    marcar_presenca,
    marcar_ausencia,
    cancelar_acao,
    campanha_create,
    campanha_update,
    campanha_delete,
    voluntarios_list,
    voluntario_create,
    voluntario_update,
    voluntario_delete,
    meu_perfil,
    ranking,
    inicio,
    inscrever_voluntario_admin,
)

urlpatterns = [
    path('inicio/', inicio, name='inicio'),

    path('acoes/', acoes_list, name='acoes_list'),
    path('acoes/nova/', acao_create, name='acao_create'),
    path('acoes/<int:acao_id>/editar/', acao_update, name='acao_update'),
    path('acoes/<int:acao_id>/inscrever/', inscrever_acao, name='inscrever_acao'),
    path('acoes/<int:acao_id>/inscritos/', inscritos_acao, name='inscritos_acao'),
    path('acoes/<int:acao_id>/cancelar/', cancelar_acao, name='cancelar_acao'),
    path('acoes/<int:acao_id>/inscrever-voluntario/', inscrever_voluntario_admin, name='inscrever_voluntario_admin'),

    path('inscricoes/<int:inscricao_id>/presenca/', marcar_presenca, name='marcar_presenca'),
    path('inscricoes/<int:inscricao_id>/ausencia/', marcar_ausencia, name='marcar_ausencia'),
    
    path('voluntarios/', voluntarios_list, name='voluntarios_list'),
    path('voluntarios/novo/', voluntario_create, name='voluntario_create'),
    path('voluntarios/<int:voluntario_id>/editar/', voluntario_update, name='voluntario_update'),
    path('voluntarios/<int:voluntario_id>/excluir/', voluntario_delete, name='voluntario_delete'),

    path('campanhas/', campanhas, name='campanhas'),
    path('campanhas/nova/', campanha_create, name='campanha_create'),
    path('campanhas/<int:campanha_id>/editar/', campanha_update, name='campanha_update'),
    path('campanhas/<int:campanha_id>/excluir/', campanha_delete, name='campanha_delete'),

    path('ranking/', ranking, name='ranking'),

    path('meu-perfil/', meu_perfil, name='meu_perfil'),
    path('minhas-inscricoes/', minhas_inscricoes, name='minhas_inscricoes'),
    path('cadastro/', cadastro_voluntario_view, name='cadastro_voluntario'),
]