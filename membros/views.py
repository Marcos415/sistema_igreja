from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
# Importação dos modelos
from .models import Celula, Membro, Reuniao, Frequencia

# --- Home e Gestão ---
def home_sistema(request):
    """Página inicial do sistema."""
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    """Página de gestão (redireciona para home ou painel)."""
    return render(request, 'membros/home_sistema.html')

# --- Gestão de Membros (CRUD) ---
def adicionar_membro(request):
    """View para adicionar novos membros."""
    return render(request, 'membros/membro_form.html')

def editar_membro(request, pk):
    """View para editar membros existentes (Corrige o erro de build)."""
    membro = get_object_or_404(Membro, pk=pk)
    return render(request, 'membros/membro_form.html', {'membro': membro})

def listar_membros(request):
    """Lista todos os membros cadastrados."""
    membros = Membro.objects.all()
    return render(request, 'membros/listar_membros.html', {'membros': membros})

# --- Frequência ---
def registrar_frequencia_reuniao(request):
    """
    Lógica para registrar presença de membros em uma reunião.
    """
    celulas = Celula.objects.all()
    
    if request.method == "POST":
        celula_id = request.POST.get('celula')
        data_reuniao = request.POST.get('data_reuniao')
        hora_reuniao = request.POST.get('hora_reuniao')
        
        celula = get_object_or_404(Celula, id=celula_id)
        reuniao, created = Reuniao.objects.get_or_create(
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

        messages.success(request, f"Frequência registrada com sucesso!")
        return redirect('registrar_frequencia_reuniao')

    return render(request, 'membros/registrar_frequencia_reuniao.html', {'celulas': celulas})