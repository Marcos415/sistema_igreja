from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Celula, Membro, Reuniao, Frequencia

# --- Home e Painel de Gestão ---
def home_sistema(request):
    """Página inicial do sistema."""
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    """Página principal de gestão."""
    return render(request, 'membros/home_sistema.html')

# --- Gestão de Membros (CRUD Completo) ---
def listar_membros(request):
    """Lista todos os membros cadastrados."""
    membros = Membro.objects.all()
    return render(request, 'membros/listar_membros.html', {'membros': membros})

def adicionar_membro(request):
    """View para adicionar novos membros."""
    return render(request, 'membros/membro_form.html')

def editar_membro(request, pk):
    """View para editar membros existentes."""
    membro = get_object_or_404(Membro, pk=pk)
    return render(request, 'membros/membro_form.html', {'membro': membro})

def membro_confirm_delete(request, pk):
    """View para confirmar a exclusão de um membro (Corrige o erro de Build)."""
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == "POST":
        membro.delete()
        messages.success(request, "Membro excluído com sucesso!")
        return redirect('listar_membros')
    return render(request, 'membros/membro_confirm_delete.html', {'membro': membro})

# --- Lógica de Frequência ---
def registrar_frequencia_reuniao(request):
    """View para registrar a presença dos membros em reuniões."""
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