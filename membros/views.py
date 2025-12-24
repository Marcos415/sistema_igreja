from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Celula, Membro, Reuniao, Frequencia

# --- Home e Gestão ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- Gestão de Membros ---
def listar_membros(request):
    membros = Membro.objects.all()
    return render(request, 'membros/listar_membros.html', {'membros': membros})

# --- Gestão de Células ---
def listar_celulas(request):
    celulas = Celula.objects.all()
    return render(request, 'membros/listar_celulas.html', {'celulas': celulas})

# --- Histórico de Frequência ---
def historico_frequencia(request):
    """Lógica para o template historico_frequencia.html que você já possui."""
    celulas = Celula.objects.all()
    datas_reuniao = Reuniao.objects.values_list('data_reuniao', flat=True).distinct()
    
    # Adicionando lógica básica para os filtros do seu template
    selected_celula_id = request.GET.get('celula_id')
    selected_data = request.GET.get('data_reuniao')
    
    # Filtro básico (pode ser expandido depois)
    historico = [] 
    
    context = {
        'celulas': celulas,
        'datas_reuniao_disponiveis': datas_reuniao,
        'historico': historico,
        'selected_celula_id': int(selected_celula_id) if selected_celula_id else None,
        'selected_data_reuniao': selected_data,
    }
    return render(request, 'membros/historico_frequencia.html', context)

def historico_frequencia_pdf(request):
    """View exigida pelo seu template para o botão de PDF."""
    return HttpResponse("Funcionalidade de PDF em desenvolvimento.")

# --- Registro de Frequência ---
def selecionar_reuniao_frequencia(request):
    """View para o template selecionar_reuniao_frequencia.html."""
    return render(request, 'membros/selecionar_reuniao_frequencia.html')

def registrar_frequencia_reuniao(request, pk=None):
    """View para o template registrar_frequencia_reuniao.html."""
    celulas = Celula.objects.all()
    return render(request, 'membros/registrar_frequencia_reuniao.html', {'celulas': celulas})