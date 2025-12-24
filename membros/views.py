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

def adicionar_membro(request):
    return render(request, 'membros/membro_form.html')

def editar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    return render(request, 'membros/membro_form.html', {'membro': membro})

def membro_confirm_delete(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == "POST":
        membro.delete()
        messages.success(request, "Membro removido!")
        return redirect('membros:listar_membros')
    return render(request, 'membros/membro_confirm_delete.html', {'membro': membro})

# --- Gestão de Células ---
def listar_celulas(request):
    celulas = Celula.objects.all()
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
        messages.success(request, "Célula removida!")
        return redirect('membros:listar_celulas')
    return render(request, 'membros/celula_confirm_delete.html', {'celula': celula})

# --- Gestão de Reuniões ---
def listar_reunioes(request):
    reunioes = Reuniao.objects.all()
    return render(request, 'membros/home_sistema.html', {'reunioes': reunioes})

def adicionar_reuniao(request):
    return render(request, 'membros/home_sistema.html')

def editar_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    return render(request, 'membros/home_sistema.html', {'reuniao': reuniao})

def reuniao_confirm_delete(request, pk):
    """Corrigido o nome para bater com o urls.py e resolver o AttributeError"""
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == "POST":
        reuniao.delete()
        messages.success(request, "Reunião removida!")
        return redirect('membros:listar_reunioes')
    return render(request, 'membros/reuniao_confirm_delete.html', {'reuniao': reuniao})

# --- Histórico e Frequência ---
def historico_frequencia(request):
    celulas = Celula.objects.all()
    return render(request, 'membros/historico_frequencia.html', {'celulas': celulas})

def historico_frequencia_pdf(request):
    return HttpResponse("Gerando PDF do histórico...")

def selecionar_reuniao_frequencia(request):
    return render(request, 'membros/selecionar_reuniao_frequencia.html')

def registrar_frequencia_reuniao(request, pk=None):
    celulas = Celula.objects.all()
    return render(request, 'membros/registrar_frequencia_reuniao.html', {'celulas': celulas})