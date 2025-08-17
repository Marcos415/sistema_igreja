from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Membro, Celula, Reuniao, Frequencia
from .forms import MembroForm, CelulaForm, ReuniaoForm, FrequenciaForm

# Importações para a geração de PDF
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.templatetags.static import static

# Para lidar com datas
from datetime import datetime

# --- Views para Membros ---

def adicionar_membro(request):
    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro adicionado com sucesso!')
            return redirect('membros:listar_membros')
    else:
        form = MembroForm()
    context = {
        'form': form,
        'titulo_pagina': 'Adicionar Membro'
    }
    return render(request, 'membros/adicionar_membro.html', context)

def listar_membros(request):
    membros = Membro.objects.all().order_by('nome_completo')
    context = {
        'membros': membros,
        'titulo_pagina': 'Lista de Membros'
    }
    return render(request, 'membros/listar_membros.html', context)

def editar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro atualizado com sucesso!')
            return redirect('membros:listar_membros')
    else:
        form = MembroForm(instance=membro)
    context = {
        'form': form,
        'membro': membro,
        'titulo_pagina': 'Editar Membro'
    }
    return render(request, 'membros/editar_membro.html', context)

def membro_confirm_delete(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        membro.delete()
        messages.success(request, 'Membro excluído com sucesso!')
        return redirect('membros:listar_membros')
    context = {
        'membro': membro,
        'titulo_pagina': 'Confirmar Exclusão de Membro'
    }
    return render(request, 'membros/membro_confirm_delete.html', context)


# --- Views para Células ---

def adicionar_celula(request):
    if request.method == 'POST':
        form = CelulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Célula adicionada com sucesso!')
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm()
    context = {
        'form': form,
        'titulo_pagina': 'Adicionar Célula'
    }
    return render(request, 'membros/adicionar_celula.html', context)

def listar_celulas(request):
    celulas = Celula.objects.all().order_by('nome')
    context = {
        'celulas': celulas,
        'titulo_pagina': 'Lista de Células'
    }
    return render(request, 'membros/listar_celulas.html', context)

def editar_celula(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == 'POST':
        form = CelulaForm(request.POST, instance=celula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Célula atualizada com sucesso!')
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm(instance=celula)
    context = {
        'form': form,
        'celula': celula,
        'titulo_pagina': 'Editar Célula'
    }
    return render(request, 'membros/editar_celula.html', context)

def celula_confirm_delete(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == 'POST':
        celula.delete()
        messages.success(request, 'Célula excluída com sucesso!')
        return redirect('membros:listar_celulas')
    context = {
        'celula': celula,
        'titulo_pagina': 'Confirmar Exclusão de Célula'
    }
    return render(request, 'membros/celula_confirm_delete.html', context)


# --- Views para Reuniões ---

def adicionar_reuniao(request):
    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reunião adicionada com sucesso!')
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm()
    context = {
        'form': form,
        'titulo_pagina': 'Adicionar Reunião'
    }
    return render(request, 'membros/adicionar_reuniao.html', context)

def listar_reunioes(request):
    reunioes = Reuniao.objects.all().order_by('-data_reuniao', '-hora_reuniao')
    context = {
        'reunioes': reunioes,
        'titulo_pagina': 'Lista de Reuniões'
    }
    return render(request, 'membros/listar_reunioes.html', context)

def editar_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reunião atualizada com sucesso!')
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm(instance=reuniao)
    context = {
        'form': form,
        'reuniao': reuniao,
        'titulo_pagina': 'Editar Reunião'
    }
    return render(request, 'membros/editar_reuniao.html', context)

def reuniao_confirm_delete(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == 'POST':
        reuniao.delete()
        messages.success(request, 'Reunião excluída com sucesso!')
        return redirect('membros:listar_reunioes')
    context = {
        'reuniao': reuniao,
        'titulo_pagina': 'Confirmar Exclusão de Reunião'
    }
    return render(request, 'membros/reuniao_confirm_delete.html', context)


# --- Views para Frequência ---

def selecionar_reuniao_frequencia(request):
    reunioes = Reuniao.objects.all().order_by('-data_reuniao', '-hora_reuniao')
    if request.method == 'POST':
        reuniao_id = request.POST.get('reuniao_id')
        if reuniao_id:
            return redirect('membros:registrar_frequencia_reuniao', pk=reuniao_id)
        else:
            messages.error(request, 'Por favor, selecione uma reunião.')
    context = {
        'reunioes': reunioes,
        'titulo_pagina': 'Selecionar Reunião para Frequência'
    }
    return render(request, 'membros/selecionar_reuniao_frequencia.html', context)


def registrar_frequencia_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    
    if reuniao.celula:
        membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome_completo')
    else:
        messages.error(request, 'Esta reunião não está associada a uma célula. Não é possível registrar frequência.')
        return redirect('membros:selecionar_reuniao_frequencia')

    if request.method == 'POST':
        frequencia_form = FrequenciaForm(request.POST, reuniao=reuniao, membros=membros)
        if frequencia_form.is_valid():
            frequencia_form.save()
            messages.success(request, 'Frequência registrada com sucesso!')
            return redirect('membros:historico_frequencia')
        else:
            messages.error(request, 'Erro ao registrar frequência. Verifique os dados.')
    else:
        frequencia_form = FrequenciaForm(reuniao=reuniao, membros=membros)

    context = {
        'reuniao': reuniao,
        'membros': membros,
        'frequencia_form': frequencia_form,
        'titulo_pagina': f'Registrar Frequência para Reunião: {reuniao.tema}'
    }
    return render(request, 'membros/registrar_frequencia_reuniao.html', context)


def historico_frequencia(request):
    # Obter filtros da requisição GET
    celula_id = request.GET.get('celula_id')
    data_reuniao_str = request.GET.get('data_reuniao')

    # Queryset base para frequências
    frequencias_qs = Frequencia.objects.all()

    # Aplicar filtro por célula, se fornecido
    if celula_id:
        frequencias_qs = frequencias_qs.filter(reuniao__celula__pk=celula_id)
    
    # Aplicar filtro por data da reunião, se fornecido
    selected_data_reuniao = None
    if data_reuniao_str:
        try:
            selected_data_reuniao = datetime.strptime(data_reuniao_str, '%Y-%m-%d').date()
            frequencias_qs = frequencias_qs.filter(reuniao__data_reuniao=selected_data_reuniao)
        except ValueError:
            messages.error(request, 'Formato de data inválido. Use AAAA-MM-DD.')

    # Agrupar frequências por membro
    membros_com_frequencia = Membro.objects.filter(frequencia__in=frequencias_qs).distinct().order_by('nome_completo')
    
    historico = []
    for membro in membros_com_frequencia:
        # Pega as frequências do membro já filtradas pelo queryset base
        frequencias_membro = frequencias_qs.filter(membro=membro).order_by('reuniao__data_reuniao', 'reuniao__hora_reuniao')
        if frequencias_membro.exists():
            historico.append({
                'membro': membro,
                'frequencias': frequencias_membro
            })

    # Obter todas as células e datas de reunião para os filtros do formulário
    celulas = Celula.objects.all().order_by('nome')
    # Obter todas as datas de reunião distintas para o filtro de data
    datas_reuniao_disponiveis = Reuniao.objects.values_list('data_reuniao', flat=True).distinct().order_by('-data_reuniao')

    context = {
        'historico': historico,
        'celulas': celulas,
        'datas_reuniao_disponiveis': datas_reuniao_disponiveis, # Passa as datas para o filtro
        'selected_celula_id': int(celula_id) if celula_id else '', # Para pré-selecionar o filtro
        'selected_data_reuniao': data_reuniao_str, # Para pré-selecionar o filtro
        'titulo_pagina': 'Histórico de Frequência'
    }
    return render(request, 'membros/historico_frequencia.html', context)


def gerar_pdf_historico_frequencia(request):
    celula_id = request.GET.get('celula_id')
    data_reuniao_str = request.GET.get('data_reuniao')
    
    celulas_para_relatorio = []

    # Queryset base para reuniões
    reunioes_qs = Reuniao.objects.all()

    # Aplicar filtro de data da reunião, se fornecido
    if data_reuniao_str:
        try:
            selected_data_reuniao = datetime.strptime(data_reuniao_str, '%Y-%m-%d').date()
            reunioes_qs = reunioes_qs.filter(data_reuniao=selected_data_reuniao)
        except ValueError:
            # Se a data for inválida, não aplica o filtro de data
            pass 

    # Aplicar filtro por célula, se fornecido
    if celula_id:
        try:
            celula_selecionada = get_object_or_404(Celula, pk=celula_id)
            # Pega apenas as reuniões da célula selecionada
            reunioes_qs = reunioes_qs.filter(celula=celula_selecionada)
            celulas_para_relatorio.append(celula_selecionada)
        except Http404:
            # Se a célula não for encontrada, não gera o PDF para ela
            celulas_para_relatorio = [] # Zera a lista para não gerar PDF
    else:
        # Se nenhum filtro de célula, pega todas as células que têm reuniões no queryset filtrado
        celulas_para_relatorio = Celula.objects.filter(reuniao__in=reunioes_qs).distinct().order_by('nome')


    celulas_com_frequencia = []
    for celula in celulas_para_relatorio:
        # Pega apenas os membros desta célula que têm frequências registradas
        membros_da_celula = Membro.objects.filter(
            celula=celula,
            frequencia__isnull=False
        ).distinct().order_by('nome_completo')
        
        membros_com_frequencia_na_celula = []

        for membro in membros_da_celula:
            # Pega apenas as frequências para este membro e para as reuniões filtradas
            frequencias_membro = Frequencia.objects.filter(
                membro=membro,
                reuniao__in=reunioes_qs.filter(celula=celula) # Filtra frequências pelas reuniões já filtradas e desta célula
            ).order_by('reuniao__data_reuniao', 'reuniao__hora_reuniao')

            # Prepara os dados para o template, convertendo o objeto Frequencia em um dicionario mais simples
            frequencias_simples = []
            for freq in frequencias_membro:
                frequencias_simples.append({
                    'data': freq.reuniao.data_reuniao,
                    'status': 'Presente' if freq.status == 'P' else 'Ausente'
                })

            if frequencias_membro.exists():
                membros_com_frequencia_na_celula.append({
                    'nome': membro.nome_completo,
                    'frequencias': frequencias_simples
                })
        
        if membros_com_frequencia_na_celula:
            celulas_com_frequencia.append({
                'nome_celula': celula.nome,
                'membros': membros_com_frequencia_na_celula
            })

    # Construindo a URL absoluta da logo
    logo_url = request.build_absolute_uri(static('img/minha_logo.png'))
    
    # Contexto para passar ao template
    contexto_pdf = {
        'celulas': celulas_com_frequencia,
        'data_geracao': datetime.now().strftime("%d/%m/%Y"),
        'logo_url': logo_url
    }

    # Renderizar o template HTML
    html_string = render_to_string('membros/relatorio.html', contexto_pdf)
    
    # Gerar o PDF a partir do HTML
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    # Criar a resposta HTTP para o download do PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historico_frequencia.pdf"'
    
    return response


# --- Outras Views (se existirem) ---
#
#def home_sistema(request):
#    context = {
#        'titulo_pagina': 'Bem-vindo IEQ CRUVIANA'
#    }
#    return render(request, 'membros/home_sistema.html', context)
#
#def gestao_view(request):
#    context = {
#        'titulo_pagina': 'Painel de Gestão'
#    }
#    return render(request, 'membros/gestao_panel.html', context)
