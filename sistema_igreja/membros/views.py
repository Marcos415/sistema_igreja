from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from weasyprint import HTML, CSS
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import base64 # Importe a biblioteca base64

# Importe outros modelos e formulários necessários
from membros.models import Membro, Celula, Frequencia, Frequencia_Membro
from membros.forms import FrequenciaForm, FrequenciaSelecaoForm

# Suas outras views...

# View para gerar o PDF da frequência
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from weasyprint import HTML, CSS
from django.contrib.staticfiles.storage import staticfiles_storage # Importação necessária
import os
import base64

# Importe outros modelos e formulários necessários
from membros.models import Membro, Celula, Frequencia, Frequencia_Membro
from membros.forms import FrequenciaForm, FrequenciaSelecaoForm

# Suas outras views...

# View para gerar o PDF da frequência
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from weasyprint import HTML, CSS
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find # Importação para a nova solução
import os
import base64

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

        # --- AQUI ESTÁ A MUDANÇA MAIS ROBUSTA ---
        # 1. Usamos a função find() para localizar o arquivo da logo de forma confiável.
        logo_path = find('img/minha_logo.png')
        
        logo_base64 = None
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, 'rb') as logo_file:
                encoded_string = base64.b64encode(logo_file.read()).decode('utf-8')
                logo_base64 = f'data:image/png;base64,{encoded_string}'
        else:
            # Esta mensagem de depuração aparecerá se o arquivo não for encontrado
            print(f"Erro: Logo não encontrada no caminho '{logo_path}'")

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
            'logo_base64': logo_base64,
        }
        
        template = get_template('membros/relatorios/relatorio_frequencia_pdf.html')
        html_string = template.render(context)
        
        html = HTML(string=html_string)

        css_path = staticfiles_storage.path('css/pdf_style.css')
        if os.path.exists(css_path):
            css = CSS(filename=css_path)
            stylesheets = [css]
        else:
            stylesheets = []

        pdf = html.write_pdf(stylesheets=stylesheets)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Frequencia_Celula_{celula.nome}_{frequencia.data_reuniao}.pdf"'
        
        return response

    except (Celula.DoesNotExist, Frequencia.DoesNotExist):
        messages.error(request, 'Frequência não encontrada para a célula e data selecionadas.')
        return redirect('historico_frequencia')



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
            'logo_base64': logo_base64, # Passe a URL de dados para o contexto.
        }
        
        template = get_template('membros/relatorios/relatorio_frequencia_pdf.html')
        html_string = template.render(context)
        
        # Cria o objeto HTML do WeasyPrint. Não precisamos de base_url aqui.
        html = HTML(string=html_string)

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
