from django.urls import path
from .views import (
    AdicionarMembroView, EditarMembroView, MembroConfirmDeleteView, ListarMembrosView,
    AdicionarCelulaView, EditarCelulaView, CelulaConfirmDeleteView, ListarCelulasView,
    AdicionarReuniaoView, EditarReuniaoView, ReuniaoConfirmDeleteView, ListarReunioesView,
    HistoricoFrequenciaView,  # Agora importamos a classe, não a função.
    selecionar_reuniao_frequencia, registrar_frequencia_reuniao,
    gerar_pdf_historico_frequencia,
    home_sistema, gestao_view
)

app_name = 'membros' 

urlpatterns = [
    # Alterando o nome da URL para 'gestao' para resolver o erro NoReverseMatch
    path('', gestao_view, name='gestao'),
    # URLs para Membros usando CBVs
    path('membros/adicionar/', AdicionarMembroView.as_view(), name='adicionar_membro'),
    path('membros/listar/', ListarMembrosView.as_view(), name='listar_membros'),
    path('membros/<int:pk>/editar/', EditarMembroView.as_view(), name='editar_membro'),
    path('membros/<int:pk>/excluir/', MembroConfirmDeleteView.as_view(), name='excluir_membro'),
    
    # URLs para Células usando CBVs
    path('celulas/adicionar/', AdicionarCelulaView.as_view(), name='adicionar_celula'),
    path('celulas/listar/', ListarCelulasView.as_view(), name='listar_celulas'),
    # CORREÇÃO: troquei 'as_as_view' para 'as_view'
    path('celulas/<int:pk>/editar/', EditarCelulaView.as_view(), name='editar_celula'),
    path('celulas/<int:pk>/excluir/', CelulaConfirmDeleteView.as_view(), name='celula_confirm_delete'),
    
    # URLs para Reuniões usando CBVs
    path('reunioes/adicionar/', AdicionarReuniaoView.as_view(), name='adicionar_reuniao'),
    path('reunioes/listar/', ListarReunioesView.as_view(), name='listar_reunioes'),
    path('reunioes/<int:pk>/editar/', EditarReuniaoView.as_view(), name='editar_reuniao'),
    path('reunioes/<int:pk>/excluir/', ReuniaoConfirmDeleteView.as_view(), name='reuniao_confirm_delete'),
    
    # URLs para Gestão de Frequência, com o Histórico agora sendo uma CBV
    path('frequencia/selecionar/', selecionar_reuniao_frequencia, name='selecionar_reuniao_frequencia'),
    path('frequencia/registrar/<int:pk>/', registrar_frequencia_reuniao, name='registrar_frequencia_reuniao'),
    path('frequencia/historico/', HistoricoFrequenciaView.as_view(), name='historico_frequencia'),
    path('frequencia/historico/pdf/', gerar_pdf_historico_frequencia, name='historico_frequencia_pdf'),

    path('home/', home_sistema, name='home_sistema'),
]
