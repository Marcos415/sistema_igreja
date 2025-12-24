from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Celula, Membro, Reuniao, Frequencia
from .forms import MembroForm, CelulaForm, ReuniaoForm
from datetime import date

# --- HOME E GESTÃO ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- GESTÃO DE MEMBROS ---
def listar_membros(request):
    membros = Membro.objects.all().order_by('nome_completo')
    return render(request, 'membros/listar_membros.html', {'membros': membros})

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
            messages.success(request, "Cadastro do membro atualizado!")
            return redirect('membros:listar_membros')
    else:
        form = MembroForm(instance=membro)
    return render(request, 'membros/membro_form.html', {'form': form, 'membro': membro})

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

def celula_confirm_delete(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == "POST":
        celula.delete()
        messages.success(request, "Célula excluída!")
        return redirect('membros:listar_celulas')
    return render(request, 'membros/celula_confirm_delete.html', {'celula': celula})

# --- GESTÃO DE REUNIÕES ---
def listar_reunioes(request):
    reunioes = Reuniao.objects.all().order_by('-data_reuniao')
    return render(request, 'membros/listar_reunioes.html', {'reunioes': reunioes})

def adicionar_reuniao(request):
    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reunião agendada!")
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm()
    return render(request, 'membros/reuniao_form.html', {'form': form})

def editar_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            form.save()
            messages.success(request, "Reunião atualizada!")
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm(instance=reuniao)
    return render(request, 'membros/reuniao_form.html', {'form': form, 'reuniao': reuniao})

def reuniao_confirm_delete(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == "POST":
        reuniao.delete()
        messages.success(request, "Reunião removida!")
        return redirect('membros:listar_reunioes')
    return render(request, 'membros/reuniao_confirm_delete.html', {'reuniao': reuniao})

# --- FREQUÊNCIA ---
def selecionar_reuniao_frequencia(request):
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
        messages.success(request, "Frequência salva!")
        return redirect('membros:home_sistema')

    frequencias_existentes = {f.membro_id: f.presente for f in Frequencia.objects.filter(reuniao=reuniao)}
    return render(request, 'membros/registrar_frequencia_reuniao.html', {
        'reuniao': reuniao, 
        'membros': membros, 
        'frequencias_existentes': frequencias_existentes
    })

# --- HISTÓRICO E PDF ---
def historico_frequencia(request):
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/historico_frequencia.html', {'celulas': celulas})

def gerar_pdf_historico_frequencia(request):
    return HttpResponse("PDF em breve.")