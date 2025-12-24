from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Celula, Membro, Reuniao, Frequencia
from .forms import MembroForm, CelulaForm, ReuniaoForm
from datetime import date
import io
from xhtml2pdf import pisa

# --- HOME E GESTÃO ---
def home_sistema(request):
    return render(request, 'membros/home_sistema.html')

def gestao_view(request):
    return render(request, 'membros/home_sistema.html')

# --- GESTÃO DE MEMBROS ---
def listar_membros(request):
    membros = Membro.objects.all().order_by('nome_completo')
    return render(request, 'membros/listar_membros.html', {'membros': membros})

def adicionar_membro(request):
    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membro cadastrado com sucesso!")
            return redirect('membros:listar_membros')
    else:
        form = MembroForm()
    return render(request, 'membros/membro_form.html', {'form': form})

def editar_membro(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro do membro atualizado!")
            return redirect('membros:listar_membros')
    else:
        form = MembroForm(instance=membro)
    return render(request, 'membros/membro_form.html', {'form': form, 'membro': m})

def membro_confirm_delete(request, pk):
    membro = get_object_or_404(Membro, pk=pk)
    if request.method == "POST":
        membro.delete()
        messages.success(request, "Membro removido!")
        return redirect('membros:listar_membros')
    return render(request, 'membros/membro_confirm_delete.html', {'membro': membro})

# --- GESTÃO DE CÉLULAS ---
def listar_celulas(request):
    celulas = Celula.objects.all().order_by('nome')
    return render(request, 'membros/listar_celulas.html', {'celulas': celulas})

def adicionar_celula(request):
    if request.method == 'POST':
        form = CelulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Célula criada com sucesso!")
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm()
    return render(request, 'membros/celula_form.html', {'form': form})

def editar_celula(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == 'POST':
        form = CelulaForm(request.POST, instance=celula)
        if form.is_valid():
            form.save()
            messages.success(request, "Célula atualizada!")
            return redirect('membros:listar_celulas')
    else:
        form = CelulaForm(instance=celula)
    return render(request, 'membros/celula_form.html', {'form': form, 'celula': celula})

def celula_confirm_delete(request, pk):
    celula = get_object_or_404(Celula, pk=pk)
    if request.method == "POST":
        celula.delete()
        messages.success(request, "Célula excluída!")
        return redirect('membros:listar_celulas')
    return render(request, 'membros/celula_confirm_delete.html', {'celula': celula})

# --- GESTÃO DE REUNIÕES ---
def listar_reunioes(request):
    reunioes = Reuniao.objects.all().order_by('-data_reuniao')
    return render(request, 'membros/listar_reunioes.html', {'reunioes': reunioes})

def adicionar_reuniao(request):
    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reunião agendada!")
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm()
    return render(request, 'membros/reuniao_form.html', {'form': form})

def editar_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            form.save()
            messages.success(request, "Reunião atualizada!")
            return redirect('membros:listar_reunioes')
    else:
        form = ReuniaoForm(instance=reuniao)
    return render(request, 'membros/reuniao_form.html', {'form': form, 'reuniao': reuniao})

def reuniao_confirm_delete(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == "POST":
        reuniao.delete()
        messages.success(request, "Reunião removida!")
        return redirect('membros:listar_reunioes')
    return render(request, 'membros/reuniao_confirm_delete.html', {'reuniao': reuniao})

# --- FREQUÊNCIA (REGISTRO) ---
def selecionar_reuniao_frequencia(request):
    reunioes = Reuniao.objects.filter(data_reuniao__lte=date.today()).order_by('-data_reuniao')
    if request.method == 'POST':
        reuniao_id = request.POST.get('reuniao_id')
        if reuniao_id:
            return redirect('membros:registrar_frequencia_reuniao', pk=reuniao_id)
    return render(request, 'membros/selecionar_reuniao_frequencia.html', {'reunioes': reunioes})

def registrar_frequencia_reuniao(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    membros = Membro.objects.filter(celula=reuniao.celula).order_by('nome_completo')

    if request.method == 'POST':
        for membro in membros:
            presente = request.POST.get(f'presenca_{membro.id}') == 'on'
            Frequencia.objects.update_or_create(
                reuniao=reuniao, membro=membro,
                defaults={'presente': presente}
            )
        messages.success(request, "Frequência salva com sucesso!")
        return redirect('membros:historico_frequencia')

    frequencias_existentes = {f.membro_id: f.presente for f in Frequencia.objects.filter(reuniao=reuniao)}
    return render(request, 'membros/registrar_frequencia_reuniao.html', {
        'reuniao': reuniao, 
        'membros': membros, 
        'frequencias_existentes': frequencias_existentes
    })

# --- HISTÓRICO E FILTROS ---
def historico_frequencia(request):
    celula_id = request.GET.get('celula_id')
    data_reuniao = request.GET.get('data_reuniao')

    celulas = Celula.objects.all().order_by('nome')
    datas_reuniao_disponiveis = Reuniao.objects.filter(
        frequencias__isnull=False
    ).values_list('data_reuniao', flat=True).distinct().order_by('-data_reuniao')

    frequencias_query = Frequencia.objects.select_related('membro', 'reuniao', 'membro__celula').all()

    if celula_id:
        frequencias_query = frequencias_query.filter(membro__celula_id=celula_id)
    if data_reuniao:
        frequencias_query = frequencias_query.filter(reuniao__data_reuniao=data_reuniao)

    membros_ids = frequencias_query.values_list('membro_id', flat=True).distinct()
    historico = []
    for m_id in membros_ids:
        membro = Membro.objects.get(pk=m_id)
        freqs = frequencias_query.filter(membro_id=m_id).order_by('-reuniao__data_reuniao')
        historico.append({'membro': membro, 'frequencias': freqs})

    context = {
        'celulas': celulas,
        'datas_reuniao_disponiveis': datas_reuniao_disponiveis,
        'historico': historico,
        'selected_celula_id': int(celula_id) if celula_id else None,
        'selected_data_reuniao': data_reuniao,
    }
    return render(request, 'membros/historico_frequencia.html', context)

# --- PDF ---
def historico_frequencia_pdf(request):
    celula_id = request.GET.get('celula_id')
    data_reuniao = request.GET.get('data_reuniao')

    celulas_list = Celula.objects.all()
    if celula_id:
        celulas_list = celulas_list.filter(pk=celula_id)

    celulas_com_frequencia = []
    for celula in celulas_list:
        membros_da_celula = Membro.objects.filter(celula=celula).order_by('nome_completo')
        membros_com_dados = []
        for membro in membros_da_celula:
            freqs = Frequencia.objects.filter(membro=membro).select_related('reuniao')
            if data_reuniao:
                freqs = freqs.filter(reuniao__data_reuniao=data_reuniao)
            if freqs.exists():
                membros_com_dados.append({'membro': membro, 'frequencias': freqs})
        if membros_com_dados:
            celulas_com_frequencia.append({'celula': celula, 'membros_da_celula': membros_com_dados})

    context = {
        'titulo_documento': 'Relatório de Frequência',
        'celulas_com_frequencia': celulas_com_frequencia,
        'selected_data_reuniao': data_reuniao,
    }

    template = get_template('membros/historico_frequencia_pdf.html')
    html = template.render(context)
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("utf-8")), dest=result)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio_frequencia.pdf"'
    return response