from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Celula, Membro, Reuniao, Frequencia
from datetime import date

# --- HOME E GESTÃO ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- GESTÃO DE MEMBROS ---
def listar_membros(request):
    # CORREÇÃO: Usando 'nome_completo' em vez de 'nome'
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

# --- GESTÃO DE REUNIÕES ---
def listar_reunioes(request):
    # CORREÇÃO: Usando 'data_reuniao' em vez de 'data'
    reunioes = Reuniao.objects.all().order_by('-data_reuniao')
    return render(request, 'membros/home_sistema.html', {'reunioes': reunioes})

# --- FREQUÊNCIA ---
def selecionar_reuniao_frequencia(request):
    # CORREÇÃO: Usando 'data_reuniao' conforme o log do FieldError
    reunioes = Reuniao.objects.filter(data_reuniao__lte=date.today()).order_by('-data_reuniao')
    
    if request.method == 'POST':
        reuniao_id = request.POST.get('reuniao_id')
        if reuniao_id:
            return redirect('membros:registrar_frequencia_reuniao', pk=reuniao_id)
            
    return render(request, 'membros/selecionar_reuniao_frequencia.html', {'reunioes': reunioes})

def registrar_frequencia_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    # CORREÇÃO: 'nome_completo' e 'celula'
    membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome_completo')

    if request.method == 'POST':
        for membro in membros:
            presente = request.POST.get(f'presenca_{membro.id}') == 'on'
            Frequencia.objects.update_or_create(
                reuniao=reuniao, membro=membro,
                defaults={'presente': presente}
            )
        messages.success(request, "Frequência salva com sucesso!")
        return redirect('membros:listar_membros')

    frequencias_existentes = {f.membro_id: f.presente for f in Frequencia.objects.filter(reuniao=reuniao)}
    
    return render(request, 'membros/registrar_frequencia_reuniao.html', {
        'reuniao': reuniao, 
        'membros': membros, 
        'frequencias_existentes': frequencias_existentes
    })

# --- HISTÓRICO ---
def historico_frequencia(request):
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/historico_frequencia.html', {'celulas': celulas})

def adicionar_celula(request): return render(request, 'membros/home_sistema.html')
def editar_celula(request, pk): return render(request, 'membros/home_sistema.html')
def adicionar_reuniao(request): return render(request, 'membros/home_sistema.html')
def editar_reuniao(request, pk): return render(request, 'membros/home_sistema.html')
def reuniao_confirm_delete(request, pk): return redirect('membros:listar_reunioes')
def gerar_pdf_historico_frequencia(request): return HttpResponse("PDF em breve.")