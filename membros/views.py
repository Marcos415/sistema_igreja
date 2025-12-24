from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Celula, Membro, Reuniao, Frequencia

# --- Vistas para Home e Gestão ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- Vistas para Membros ---
def adicionar_membro(request):
    # Por enquanto renderiza o formulário existente na sua pasta
    return render(request, 'membros/membro_form.html')

def listar_membros(request):
    membros = Membro.objects.all()
    return render(request, 'membros/listar_membros.html', {'membros': membros})

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