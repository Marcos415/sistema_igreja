from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Membro, Celula, Frequencia, Reuniao
from django.utils import timezone

def registrar_frequencia_reuniao(request):
    """
    View para registrar a presença dos membros em uma reunião específica.
    """
    celulas = Celula.objects.all()
    
    if request.method == "POST":
        celula_id = request.POST.get('celula')
        data_reuniao = request.POST.get('data_reuniao')
        hora_reuniao = request.POST.get('hora_reuniao')
        
        # 1. Busca ou cria a Reunião
        celula = get_object_or_404(Celula, id=celula_id)
        reuniao, created = Reuniao.objects.get_or_create(
            celula=celula,
            data_reuniao=data_reuniao,
            hora_reuniao=hora_reuniao
        )

        # 2. Processa a lista de membros daquela célula
        membros_da_celula = Membro.objects.filter(celula=celula)
        
        for membro in membros_da_celula:
            # Verifica se o checkbox de presença foi marcado para este membro
            presenca_key = f'presenca_{membro.id}'
            esta_presente = request.POST.get(presenca_key) == 'on'
            
            # 3. Salva ou atualiza a Frequencia (usando o nome correto do modelo)
            Frequencia.objects.update_or_create(
                reuniao=reuniao,
                membro=membro,
                defaults={'presente': esta_presente}
            )

        messages.success(request, f"Frequência da célula {celula.nome} registrada com sucesso!")
        return redirect('registrar_frequencia_reuniao')

    return render(request, 'membros/registrar_frequencia_reuniao.html', {'celulas': celulas})