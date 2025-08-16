# C:\sistema_igreja\membros\urls.py

from django.urls import path
from . import views # Importa todas as views do seu arquivo views.py

app_name = 'membros' # Define o namespace da aplicação. Essencial para {% url 'membros:nome_da_url' %}

urlpatterns = [
    # URLs para a página inicial da gestão (home do sistema)
    # Esta URL é acessada via /gestao/ (por causa do include em sistema_igreja/urls.py)
    path('', views.home_sistema, name='home_sistema'), # Página inicial da sua app de membros

    # URL para o painel de gestão geral (se for uma página de menu, por exemplo)
    path('gestao/', views.gestao_view, name='gestao'),

    # URLs para Membros
    path('membros/adicionar/', views.adicionar_membro, name='adicionar_membro'),
    path('membros/listar/', views.listar_membros, name='listar_membros'),
    path('membros/<int:pk>/editar/', views.editar_membro, name='editar_membro'),
    path('membros/<int:pk>/excluir/', views.membro_confirm_delete, name='excluir_membro'),

    # URLs para Células
    path('celulas/adicionar/', views.adicionar_celula, name='adicionar_celula'),
    path('celulas/listar/', views.listar_celulas, name='listar_celulas'),
    path('celulas/<int:pk>/editar/', views.editar_celula, name='editar_celula'),
    path('celulas/<int:pk>/excluir/', views.celula_confirm_delete, name='celula_confirm_delete'),
    
    # URLs para Reuniões
    path('reunioes/adicionar/', views.adicionar_reuniao, name='adicionar_reuniao'),
    path('reunioes/listar/', views.listar_reunioes, name='listar_reunioes'),
    path('reunioes/<int:pk>/editar/', views.editar_reuniao, name='editar_reuniao'),
    path('reunioes/<int:pk>/excluir/', views.reuniao_confirm_delete, name='reuniao_confirm_delete'),

    # URLs para Gestão de Frequência
    path('frequencia/selecionar/', views.selecionar_reuniao_frequencia, name='selecionar_reuniao_frequencia'),
    path('frequencia/registrar/<int:pk>/', views.registrar_frequencia_reuniao, name='registrar_frequencia_reuniao'),
    path('frequencia/historico/', views.historico_frequencia, name='historico_frequencia'),
    path('frequencia/historico/pdf/', views.gerar_pdf_historico_frequencia, name='historico_frequencia_pdf'), # URL para gerar o PDF
]
