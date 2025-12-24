from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Celula, Membro, Reuniao, Frequencia
from .forms import MembroForm, CelulaForm, ReuniaoForm # Importa os forms do seu forms.py
from datetime import date

# --- HOME E GESTÃO ---
def home_sistema(request):
    """Página inicial do sistema de gestão."""
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    """Redireciona para a home do sistema."""
    return render(request, 'membros/home_sistema.html')

# --- GESTÃO DE MEMBROS ---
def listar_membros(request):
    """Lista todos os membros cadastrados."""
    membros = Membro.objects.all().order_by('nome_completo')
    return render(request, 'membros/listar_membros.html', {'membros': membros})

def adicionar_membro(request):
    """Processa o formulário para criar um novo membro."""
    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membro cadastrado com sucesso!")
            return redirect('membros:listar_membros')
    else:
        form = MembroForm()
    return render(request, 'membros/membro_form.html', {'form': form})

def editar_membro(request, pk):
    """Processa a edição de um membro existente."""
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro do membro atualizado!")
            return redirect('membros:listar_membros')
    else:
        form = MembroForm(instance=membro)
    return render(request, 'membros/membro_form.html', {'form': form, 'membro': membro})

def membro_confirm_delete(request, pk):
    """Exclui um membro após confirmação."""
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == "POST":
        membro.delete()
        messages.success(request, "Membro removido com sucesso!")
        return redirect('membros:listar_membros')
    return render(request, 'membros/membro_confirm_delete.html', {'membro': membro})

# --- GESTÃO DE CÉLULAS ---
def listar_celulas(request):
    """Lista todas as células cadastradas."""
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/listar_celulas.html', {'celulas': celulas})

def adicionar_celula(request):
    """Processa o formulário para criar uma nova célula."""
    if request.method == 'POST':
        form = CelulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Célula criada com sucesso!")
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm()
    return render(request, 'membros/celula_form.html', {'form': form})

def editar_celula(request, pk):
    """Processa a edição de uma célula existente."""
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == 'POST':
        form = CelulaForm(request.POST, instance=celula)
        if form.is_valid():
            form.save()
            messages.success(request, "Célula atualizada com sucesso!")
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm(instance=celula)
    return render(request, 'membros/celula_form.html', {'form': form, 'celula': celula})

def celula_confirm_delete(request, pk):
    """Exclui uma célula após confirmação."""
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == "POST":
        celula.delete()
        messages.success(request, "Célula excluída!")
        return redirect('membros:listar_celulas')
    return render(request, 'membros/celula_confirm_delete.html', {'celula': celula})

# --- GESTÃO DE REUNIÕES ---
def listar_reunioes(request):
    """Lista todas as reuniões."""
    reunioes = Reuniao.objects.all().order_by('-data_reuniao')
    return render(request, 'membros/listar_reunioes.html', {'reunioes': reunioes})

def adicionar_reuniao(request):
    """Adiciona uma nova reunião."""
    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reunião agendada!")
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm()
    return render(request, 'membros/reuniao_form.html', {'form': form})

# --- FREQUÊNCIA ---
def selecionar_reuniao_frequencia(request):
    """Lista reuniões para o usuário escolher qual marcar frequência."""
    reunioes = Reuniao.objects.filter(data_reuniao__lte=date.today()).order_by('-data_reuniao')
    if request.method == 'POST':
        reuniao_id = request.POST.get('reuniao_id')
        if reuniao_id:
            return redirect('membros:registrar_frequencia_reuniao', pk=reuniao_id)
    return render(request, 'membros/selecionar_reuniao_frequencia.html', {'reunioes': reunioes})

def registrar_frequencia_reuniao(request, pk):
    """Registra a presença dos membros em uma reunião específica."""
    reuniao = get_object_or_404(Reuniao, pk=pk)
    membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome_completo')

    if request.method == 'POST':
        for membro in membros:
            presente = request.POST.get(f'presenca_{membro.id}') == 'on'
            Frequencia.objects.update_or_create(
                reuniao=reuniao, membro=membro,
                defaults={'presente': presente}
            )
        messages.success(request, "Lista de presença salva com sucesso!")
        return redirect('membros:home_sistema')

    frequencias_existentes = {f.membro_id: f.presente for f in Frequencia.objects.filter(reuniao=reuniao)}
    return render(request, 'membros/registrar_frequencia_reuniao.html', {
        'reuniao': reuniao, 
        'membros': membros, 
        'frequencias_existentes': frequencias_existentes
    })

# --- HISTÓRICO E PDF ---
def historico_frequencia(request):
    """Exibe o histórico de frequências."""
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/historico_frequencia.html', {'celulas': celulas})

def gerar_pdf_historico_frequencia(request):
    """Gera relatório em PDF (Stub)."""
    return HttpResponse("Funcionalidade de PDF em desenvolvimento.")