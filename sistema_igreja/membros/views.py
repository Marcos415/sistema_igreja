from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from weasyprint import HTML, CSS
from django.contrib.staticfiles.storage import staticfiles_storage
import os

# Importe outros modelos e formulários necessários
from membros.models import Membro, Celula, Frequencia, Frequencia_Membro
from membros.forms import FrequenciaForm, FrequenciaSelecaoForm

# Suas outras views...

# View para gerar o PDF da frequência
def gerar_frequencia_pdf(request, celula_id, data_reuniao):
    try:
        celula = Celula.objects.get(id=celula_id)
        frequencia = Frequencia.objects.get(celula=celula, data_reuniao=data_reuniao)
        frequencia_membros = Frequencia_Membro.objects.filter(frequencia=frequencia)

        # Adicione o código para calcular os totais
        total_presentes = frequencia_membros.filter(status='Presente').count()
        total_ausentes = frequencia_membros.filter(status='Ausente').count()
        total_nao_membros = frequencia_membros.filter(status='Não membro').count()
        total_membros = total_presentes + total_ausentes
        total_celula = total_membros + total_nao_membros

        # URL base para os arquivos estáticos, para WeasyPrint
        static_url = request.build_absolute_uri(settings.STATIC_URL)

        # Renderiza o template HTML
        context = {
            'celula': celula,
            'frequencia': frequencia,
            'frequencia_membros': frequencia_membros,
            'total_presentes': total_presentes,
            'total_ausentes': total_ausentes,
            'total_nao_membros': total_nao_membros,
            'total_membros': total_membros,
            'total_celula': total_celula,
        }
        
        template = get_template('membros/pdf/frequencia.html')
        html_string = template.render(context)
        
        # Cria o objeto HTML do WeasyPrint, passando a URL base dos arquivos estáticos
        html = HTML(string=html_string, base_url=static_url)

        # Define o caminho do CSS
        css_path = staticfiles_storage.path('css/pdf_style.css')
        css = CSS(filename=css_path)

        # Gera o PDF
        pdf = html.write_pdf(stylesheets=[css])
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Frequencia_Celula_{celula.nome}_{frequencia.data_reuniao}.pdf"'
        
        return response

    except (Celula.DoesNotExist, Frequencia.DoesNotExist):
        messages.error(request, 'Frequência não encontrada para a célula e data selecionadas.')
        return redirect('historico_frequencia')
