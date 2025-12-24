from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Celula, Membro, Reuniao, Frequencia
from datetime import date

# --- HOME E GESTÃO ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

# ESSA É A FUNÇÃO QUE ESTAVA FALTANDO NO SEU ERRO:
def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- GESTÃO DE MEMBROS ---
def listar_membros(request):
    membros = Membro.objects.all().order_by('nome_completo')
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

# --- GESTÃO DE CÉLULAS ---
def listar_celulas(request):
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/listar_celulas.html', {'celulas': celulas})

def adicionar_celula(request):
    return render(request, 'membros/home_sistema.html')

def celula_confirm_delete(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == "POST":
        celula.delete()
        messages.success(request, "Célula removida!")
        return redirect('membros:listar_celulas')
    return render(request, 'membros/celula_confirm_delete.html', {'celula': celula})

# --- REUNIÕES E FREQUÊNCIA ---
def selecionar_reuniao_frequencia(request):
    # Usando o campo correto 'data_reuniao'
    reunioes = Reuniao.objects.filter(data_reuniao__lte=date.today()).order_by('-data_reuniao')
    if request.method == 'POST':
        reuniao_id = request.POST.get('reuniao_id')
        if reuniao_id:
            return redirect('membros:registrar_frequencia_reuniao', pk=reuniao_id)
    return render(request, 'membros/selecionar_reuniao_frequencia.html', {'reunioes': reunioes})

def registrar_frequencia_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome_completo')

    if request.method == 'POST':
        for membro in membros:
            presente = request.POST.get(f'presenca_{membro.id}') == 'on'
            Frequencia.objects.update_or_create(
                reuniao=reuniao, membro=membro,
                defaults={'presente': presente}
            )
        messages.success(request, "Frequência registrada!")
        return redirect('membros:listar_membros')

    # Dicionário para marcar quem já está presente ao carregar a página
    frequencias_existentes = {f.membro_id: f.presente for f in Frequencia.objects.filter(reuniao=reuniao)}
    
    return render(request, 'membros/registrar_frequencia_reuniao.html', {
        'reuniao': reuniao, 
        'membros': membros, 
        'frequencias_existentes': frequencias_existentes
    })

# --- OUTROS ---
def historico_frequencia(request):
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/historico_frequencia.html', {'celulas': celulas})

def listar_reunioes(request): return redirect('membros:selecionar_reuniao_frequencia')
def adicionar_reuniao(request): return render(request, 'membros/home_sistema.html')
def editar_reuniao(request, pk): return render(request, 'membros/home_sistema.html')
def reuniao_confirm_delete(request, pk): return redirect('membros:listar_membros')
def gerar_pdf_historico_frequencia(request): return HttpResponse("PDF em breve.")