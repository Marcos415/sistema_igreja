from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
# Importação correta dos modelos conforme seu arquivo models.py
from .models import Celula, Membro, Reuniao, Frequencia

def home_sistema(request):
    """Página inicial configurada em membros/urls.py"""
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    """Página de gestão exigida pelo seu urls.py"""
    return render(request, 'membros/home_sistema.html')

def adicionar_membro(request):
    """View para adicionar membros (exigida pelo erro do Render)"""
    # Por enquanto, redireciona ou renderiza um template se ele existir
    return render(request, 'membros/membro_form.html')

def registrar_frequencia_reuniao(request):
    """View principal para registro de presença"""
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