import os
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find

# Importação dos modelos e formulários
from membros.models import Membro, Celula, Frequencia, Frequencia_Membro, Reuniao
from membros.forms import FrequenciaForm, FrequenciaSelecaoForm

def home(request):
    """View para a página inicial."""
    return render(request, 'membros/home_sistema.html')

def listar_membros(request):
    """View para listar os membros."""
    membros = Membro.objects.all()
    context = {'membros': membros}
    return render(request, 'membros/listar_membros.html', context)

def registrar_frequencia_reuniao(request, pk):
    """Regista a frequência dos membros em uma reunião específica."""
    reuniao = get_object_or_404(Reuniao, pk=pk)
    
    # Busca os membros da célula vinculada a essa reunião
    membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome')

    if request.method == 'POST':
        for membro in membros:
            # Captura o status do checkbox enviado pelo HTML
            valor_presenca = request.POST.get(f'presenca_{membro.id}')
            status = 'Presente' if valor_presenca == 'on' else 'Ausente'
            
            # Cria ou atualiza o registro de frequência
            Frequencia_Membro.objects.update_or_create(
                reuniao=reuniao, 
                membro=membro, 
                defaults={'status': status}
            )
        
        messages.success(request, 'Frequência salva com sucesso!')
        return redirect('membros:listar_reunioes')

    context = {
        'reuniao': reuniao,
        'membros': membros,
    }
    
    # CAMINHO CORRIGIDO: pasta_app/nome_arquivo.html
    return render(request, 'membros/registrar_frequencia_reuniao.html', context)

def gerar_frequencia_pdf(request, celula_id, data_reuniao):
    """Gera um relatório de frequência em formato PDF."""
    try:
        celula = Celula.objects.get(id=celula_id)
        frequencia = Frequencia.objects.get(celula=celula, data_reuniao=data_reuniao)
        frequencia_membros = Frequencia_Membro.objects.filter(frequencia=frequencia)

        logo_path = find('img/minha_logo.png')
        logo_base64 = None
        
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, 'rb') as logo_file:
                encoded_string = base64.b64encode(logo_file.read()).decode('utf-8')
                logo_base64 = f'data:image/png;base64,{encoded_string}'

        context = {
            'celula': celula,
            'frequencia': frequencia,
            'frequencia_membros': frequencia_membros,
            'logo_base64': logo_base64,
        }
        
        template = get_template('membros/relatorios/relatorio_frequencia_pdf.html')
        html_string = template.render(context)
        
        from weasyprint import HTML
        pdf = HTML(string=html_string).write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Frequencia_{celula.nome}.pdf"'
        return response

    except Exception as e:
        messages.error(request, f'Erro ao gerar relatório: {e}')
        return redirect('membros:home')