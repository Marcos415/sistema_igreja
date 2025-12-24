from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Celula, Membro, Reuniao, Frequencia
from .forms import MembroForm, CelulaForm, ReuniaoForm # Importando seus formulários
from datetime import date

# --- GESTÃO DE MEMBROS (SALVAR E EDITAR) ---
def adicionar_membro(request):
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
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro atualizado!")
            return redirect('membros:listar_membros')
    else:
        form = MembroForm(instance=membro)
    return render(request, 'membros/membro_form.html', {'form': form, 'membro': membro})

# --- GESTÃO DE CÉLULAS (SALVAR E EDITAR) ---
def adicionar_celula(request):
    if request.method == 'POST':
        form = CelulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Célula criada!")
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm()
    return render(request, 'membros/celula_form.html', {'form': form})

def editar_celula(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == 'POST':
        form = CelulaForm(request.POST, instance=celula)
        if form.is_valid():
            form.save()
            messages.success(request, "Célula atualizada!")
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm(instance=celula)
    return render(request, 'membros/celula_form.html', {'form': form, 'celula': celula})