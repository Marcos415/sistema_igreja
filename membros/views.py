from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Celula, Membro, Reuniao, Frequencia
from datetime import date

# --- HOME E GESTÃO ---
def home_sistema(request):
    """Página inicial do sistema"""
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    """Redireciona para a home da gestão"""
    return render(request, 'membros/home_sistema.html')

# --- GESTÃO DE MEMBROS ---
def listar_membros(request):
    membros = Membro.objects.all().order_by('nome')
    return render(request, 'membros/listar_membros.html', {'membros': membros})

def adicionar_membro(request):
    # Lógica de formulário pode ser adicionada aqui posteriormente
    return render(request, 'membros/membro_form.html')

def editar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    return render(request, 'membros/membro_form.html', {'membro': membro})

def membro_confirm_delete(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == "POST":
        membro.delete()
        messages.success(request, "Membro removido com sucesso!")
        return redirect('membros:listar_membros')
    return render(request, 'membros/membro_confirm_delete.html', {'membro': membro})

# --- GESTÃO DE CÉLULAS ---
def listar_celulas(request):
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/listar_celulas.html', {'celulas': celulas})

def adicionar_celula(request):
    return render(request, 'membros/home_sistema.html')

def editar_celula(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    return render(request, 'membros/home_sistema.html', {'celula': celula})

def celula_confirm_delete(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == "POST":
        celula.delete()
        messages.success(request, "Célula removida com sucesso!")
        return redirect('membros:listar_celulas')
    return render(request, 'membros/celula_confirm_delete.html', {'celula': celula})

# --- GESTÃO DE REUNIÕES ---
def listar_reunioes(request):
    reunioes = Reuniao.objects.all().order_by('-data')
    return render(request, 'membros/home_sistema.html', {'reunioes': reunioes})

def adicionar_reuniao(request):
    return render(request, 'membros/home_sistema.html')

def editar_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    return render(request, 'membros/home_sistema.html', {'reuniao': reuniao})

def reuniao_confirm_delete(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == "POST":
        reuniao.delete()
        messages.success(request, "Reunião removida com sucesso!")
        return redirect('membros:listar_reunioes')
    return render(request, 'membros/reuniao_confirm_delete.html', {'reuniao': reuniao})

# --- FREQUÊNCIA (CORREÇÃO DA IMAGEM) ---
def selecionar_reuniao_frequencia(request):
    """
    Lista as reuniões para o usuário escolher qual frequência registrar.
    Filtra reuniões até a data atual.
    """
    reunioes = Reuniao.objects.filter(data__lte=date.today()).order_by('-data', '-horario_inicio')
    
    if request.method == 'POST':
        reuniao_id = request.POST.get('reuniao_id')
        if reuniao_id:
            return redirect('membros:registrar_frequencia_reuniao', pk=reuniao_id)
            
    return render(request, 'membros/selecionar_reuniao_frequencia.html', {
        'reunioes': reunioes,
        'titulo_pagina': 'Selecionar Reunião para Frequência'
    })

def registrar_frequencia_reuniao(request, pk):
    """
    Busca os membros da célula daquela reunião e salva a presença.
    Resolve o erro de exibição de texto puro.
    """
    reuniao = get_object_or_404(Reuniao, pk=pk)
    # Busca apenas os membros que pertencem à célula desta reunião específica
    membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome')

    if request.method == 'POST':
        for membro in membros:
            # O nome do campo no HTML deve ser f"presenca_{membro.id}"
            valor_presenca = request.POST.get(f'presenca_{membro.id}')
            esta_presente = valor_presenca == 'on'
            
            Frequencia.objects.update_or_create(
                reuniao=reuniao,
                membro=membro,
                defaults={'presente': esta_presente}
            )
        messages.success(request, f"Frequência de {reuniao.celula.nome} salva!")
        return redirect('membros:listar_reunioes')

    # Busca frequências já salvas para marcar o que já foi preenchido
    frequencias_existentes = {
        f.membro_id: f.presente 
        for f in Frequencia.objects.filter(reuniao=reuniao)
    }
    
    context = {
        'reuniao': reuniao,
        'membros': membros,
        'frequencias_existentes': frequencias_existentes,
        'titulo_pagina': f'Registrar Frequência - {reuniao.celula.nome}'
    }
    return render(request, 'membros/registrar_frequencia_reuniao.html', context)

# --- HISTÓRICO E EXPORTAÇÃO ---
def historico_frequencia(request):
    celulas = Celula.objects.all()
    return render(request, 'membros/historico_frequencia.html', {'celulas': celulas})

def gerar_pdf_historico_frequencia(request):
    """Função para exportar o histórico em PDF"""
    return HttpResponse("Funcionalidade de PDF em manutenção.")