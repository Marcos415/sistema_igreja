from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Celula, Membro, Reuniao, Frequencia

# --- Home e Gestão ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- Gestão de Membros ---
def listar_membros(request):
    membros = Membro.objects.all()
    return render(request, 'membros/listar_membros.html', {'membros': m heroes})

def adicionar_membro(request):
    return render(request, 'membros/membro_form.html')

def editar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    return render(request, 'membros/membro_form.html', {'membro': membro})

def membro_confirm_delete(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == "POST":
        membro.delete()
        return redirect('listar_membros')
    return render(request, 'membros/membro_confirm_delete.html', {'membro': membro})

# --- Gestão de Células (Resolve o novo erro do Render) ---
def listar_celulas(request):
    celulas = Celula.objects.all()
    return render(request, 'membros/listar_celulas.html', {'celulas': celulas})

def adicionar_celula(request):
    return render(request, 'membros/home_sistema.html') # Pode ajustar o template depois

def editar_celula(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    return render(request, 'membros/home_sistema.html')

# --- Lógica de Frequência ---
def registrar_frequencia_reuniao(request):
    celulas = Celula.objects.all()
    
    if request.method == "POST":
        celula_id = request.POST.get('celula')
        data_reuniao = request.POST.get('data_reuniao')
        hora_reuniao = request.POST.get('hora_reuniao')
        
        celula = get_object_or_404(Celula, id=celula_id)
        reuniao, _ = Reuniao.objects.get_or_create(
            celula=celula,
            data_reuniao=data_reuniao,
            hora_reuniao=hora_reuniao
        )

        membros_da_celula = Membro.objects.filter(celula=celula)
        for membro in membros_da_celula:
            presenca_key = f'presenca_{membro.id}'
            esta_presente = request.POST.get(presenca_key) == 'on'
            
            Frequencia.objects.update_or_create(
                reuniao=reuniao,
                membro=membro,
                defaults={'presente': esta_presente}
            )

        messages.success(request, "Frequência registrada com sucesso!")
        return redirect('registrar_frequencia_reuniao')

    return render(request, 'membros/registrar_frequencia_reuniao.html', {'celulas': celulas})