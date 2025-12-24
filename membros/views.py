from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
# Importação dos seus modelos (conforme seu models.py)
from .models import Celula, Membro, Reuniao, Frequencia

def home_sistema(request):
    """
    Página inicial. 
    Ajustado para o seu arquivo: home_sistema.html
    """
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    """
    Página de gestão. 
    Como você disse que tem outro nome, estou usando o nome que o seu urls.py pede.
    """
    # Se você tiver um HTML específico para gestão, troque o nome abaixo
    return render(request, 'membros/home_sistema.html') 

def registrar_frequencia_reuniao(request):
    """View para registrar a presença dos membros."""
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

        messages.success(request, f"Frequência da célula {celula.nome} registrada com sucesso!")
        return redirect('registrar_frequencia_reuniao')

    return render(request, 'membros/registrar_frequencia_reuniao.html', {'celulas': celulas})