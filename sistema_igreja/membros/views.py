import os
import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find # Importação para a nova solução do caminho do arquivo

# Importe seus modelos e formulários aqui
from membros.models import Membro, Celula, Frequencia, Frequencia_Membro
from membros.forms import FrequenciaForm, FrequenciaSelecaoForm

# Suas views existentes (manter inalteradas)
# Exemplo de uma view:
def home(request):
    """
    View para a página inicial.
    """
    return render(request, 'membros/home.html')

def listar_membros(request):
    """
    View para listar os membros.
    """
    membros = Membro.objects.all()
    context = {'membros': membros}
    return render(request, 'membros/listar_membros.html', context)

# ... Outras views do seu projeto ...

# View para gerar o PDF da frequência (código atualizado)
def gerar_frequencia_pdf(request, celula_id, data_reuniao):
    """
    Gera um relatório de frequência em formato PDF.
    
    Tenta encontrar o arquivo da logo usando a função `find()` do Django,
    que é a maneira mais robusta de localizar arquivos estáticos em ambientes de produção.
    A logo é então convertida para Base64 para ser incorporada diretamente no PDF.
    """
    try:
        celula = Celula.objects.get(id=celula_id)
        frequencia = Frequencia.objects.get(celula=celula, data_reuniao=data_reuniao)
        frequencia_membros = Frequencia_Membro.objects.filter(frequencia=frequencia)

        # Cálculo dos totais para o relatório
        total_presentes = frequencia_membros.filter(status='Presente').count()
        total_ausentes = frequencia_membros.filter(status='Ausente').count()
        total_nao_membros = frequencia_membros.filter(status='Não membro').count()
        total_membros = total_presentes + total_ausentes
        total_celula = total_membros + total_nao_membros

        # --- AQUI ESTÁ A MUDANÇA PRINCIPAL E MAIS ROBUSTA ---
        # 1. Usamos a função find() para localizar o caminho do arquivo da logo.
        #    Isso garante que o caminho seja o correto no ambiente do Render.
        logo_path = find('img/minha_logo.png')
        
        logo_base64 = None
        # 2. Verificamos se o arquivo foi encontrado e existe antes de tentar lê-lo.
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, 'rb') as logo_file:
                # 3. Codificamos a imagem em Base64 para incorporação direta.
                encoded_string = base64.b64encode(logo_file.read()).decode('utf-8')
                logo_base64 = f'data:image/png;base64,{encoded_string}'
        else:
            # Mensagem de depuração que aparecerá nos logs do Render se o arquivo não for encontrado.
            print(f"Erro: Logo não encontrada no caminho '{logo_path}'")

        # Configuração do contexto para o template
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
        
        # Renderização do template HTML para PDF
        template = get_template('membros/relatorios/relatorio_frequencia_pdf.html')
        html_string = template.render(context)
        
        from weasyprint import HTML, CSS
        html = HTML(string=html_string)

        # Encontra o caminho do arquivo CSS estático
        css_path = staticfiles_storage.path('css/pdf_style.css')
        if os.path.exists(css_path):
            css = CSS(filename=css_path)
            stylesheets = [css]
        else:
            stylesheets = []

        # Geração do PDF
        pdf = html.write_pdf(stylesheets=stylesheets)
        
        # Resposta HTTP com o PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Frequencia_Celula_{celula.nome}_{frequencia.data_reuniao}.pdf"'
        
        return response

    except (Celula.DoesNotExist, Frequencia.DoesNotExist):
        messages.error(request, 'Frequência não encontrada para a célula e data selecionadas.')
        return redirect('historico_frequencia')
