from django.urls import path
from . import views

app_name = 'membros'

urlpatterns = [
    # Home e Gestão
    path('', views.home_sistema, name='home_sistema'),
    path('gestao/', views.gestao_view, name='gestao'),

    # Membros
    path('membros/', views.listar_membros, name='listar_membros'),
    path('membros/novo/', views.adicionar_membro, name='adicionar_membro'),
    path('membros/<int:pk>/editar/', views.editar_membro, name='editar_membro'),
    path('membros/<int:pk>/deletar/', views.membro_confirm_delete, name='membro_confirm_delete'),

    # Células
    path('celulas/', views.listar_celulas, name='listar_celulas'),
    path('celulas/nova/', views.adicionar_celula, name='adicionar_celula'),
    path('celulas/<int:pk>/editar/', views.editar_celula, name='editar_celula'),
    path('celulas/<int:pk>/deletar/', views.celula_confirm_delete, name='celula_confirm_delete'),

    # Reuniões
    path('reunioes/', views.listar_reunioes, name='listar_reunioes'),
    path('reunioes/nova/', views.adicionar_reuniao, name='adicionar_reuniao'),
    path('reunioes/<int:pk>/editar/', views.editar_reuniao, name='editar_reuniao'),
    # path('reunioes/<int:pk>/deletar/', views.reuniao_confirm_delete, name='reuniao_confirm_delete'), # Opcional

    # Frequência (Registro)
    path('frequencia/selecionar/', views.selecionar_reuniao_frequencia, name='selecionar_reuniao_frequencia'),
    path('frequencia/registrar/<int:pk>/', views.registrar_frequencia_reuniao, name='registrar_frequencia_reuniao'),

    # Histórico e PDF (Atenção aqui!)
    path('frequencia/historico/', views.historico_frequencia, name='historico_frequencia'),
    path('frequencia/historico/pdf/', views.historico_frequencia_pdf, name='historico_frequencia_pdf'),
]