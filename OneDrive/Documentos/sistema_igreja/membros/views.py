# Importações necessárias para as Views Baseadas em Classes.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import Membro, Celula, Reuniao, Frequencia
from .forms import MembroForm, CelulaForm, ReuniaoForm, FrequenciaForm
from datetime import datetime

# Importações para a geração de PDF (mantidas)
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from weasyprint import HTML

# --- Views Refatoradas para Membros (usando CBVs) ---
class AdicionarMembroView(CreateView):
    model = Membro
    form_class = MembroForm
    template_name = 'membros/adicionar_membro.html'
    success_url = reverse_lazy('membros:listar_membros')

    def form_valid(self, form):
        messages.success(self.request, 'Membro adicionado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Membro'
        return context

class EditarMembroView(UpdateView):
    model = Membro
    form_class = MembroForm
    template_name = 'membros/editar_membro.html'
    success_url = reverse_lazy('membros:listar_membros')

    def form_valid(self, form):
        messages.success(self.request, 'Membro atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Membro'
        return context

class MembroConfirmDeleteView(DeleteView):
    model = Membro
    template_name = 'membros/membro_confirm_delete.html'
    success_url = reverse_lazy('membros:listar_membros')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Confirmar Exclusão de Membro'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Membro excluído com sucesso!')
        return super().form_valid(form)

class ListarMembrosView(ListView):
    model = Membro
    template_name = 'membros/listar_membros.html'
    context_object_name = 'membros'
    ordering = ['nome_completo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Lista de Membros'
        return context


# --- Views Refatoradas para Células (usando CBVs) ---
class AdicionarCelulaView(CreateView):
    model = Celula
    form_class = CelulaForm
    template_name = 'membros/adicionar_celula.html'
    success_url = reverse_lazy('membros:listar_celulas')

    def form_valid(self, form):
        messages.success(self.request, 'Célula adicionada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Célula'
        return context

class EditarCelulaView(UpdateView):
    model = Celula
    form_class = CelulaForm
    template_name = 'membros/editar_celula.html'
    success_url = reverse_lazy('membros:listar_celulas')

    def form_valid(self, form):
        messages.success(self.request, 'Célula atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Célula'
        return context

class CelulaConfirmDeleteView(DeleteView):
    model = Celula
    template_name = 'membros/celula_confirm_delete.html'
    success_url = reverse_lazy('membros:listar_celulas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Confirmar Exclusão de Célula'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Célula excluída com sucesso!')
        return super().form_valid(form)

class ListarCelulasView(ListView):
    model = Celula
    template_name = 'membros/listar_celulas.html'
    context_object_name = 'celulas'
    ordering = ['nome']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Lista de Células'
        return context


# --- Views Refatoradas para Reuniões (usando CBVs) ---
class AdicionarReuniaoView(CreateView):
    model = Reuniao
    form_class = ReuniaoForm
    template_name = 'membros/adicionar_reuniao.html'
    success_url = reverse_lazy('membros:listar_reunioes')

    def form_valid(self, form):
        messages.success(self.request, 'Reunião adicionada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Reunião'
        return context

class EditarReuniaoView(UpdateView):
    model = Reuniao
    form_class = ReuniaoForm
    template_name = 'membros/editar_reuniao.html'
    success_url = reverse_lazy('membros:listar_reunioes')
    
    def form_valid(self, form):
        messages.success(self.request, 'Reunião atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Reunião'
        return context

class ReuniaoConfirmDeleteView(DeleteView):
    model = Reuniao
    template_name = 'membros/reuniao_confirm_delete.html'
    success_url = reverse_lazy('membros:listar_reunioes')

    def form_valid(self, form):
        messages.success(self.request, 'Reunião excluída com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Confirmar Exclusão de Reunião'
        return context

class ListarReunioesView(ListView):
    model = Reuniao
    template_name = 'membros/listar_reunioes.html'
    context_object_name = 'reunioes'
    ordering = ['-data_reuniao', '-hora_reuniao']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Lista de Reuniões'
        return context


# --- Views Refatoradas para Frequência (usando CBVs e mantendo funções para lógica complexa) ---

class HistoricoFrequenciaView(ListView):
    # Não há um modelo principal para a view, o queryset será construído dinamicamente.
    model = Frequencia
    template_name = 'membros/historico_frequencia.html'
    context_object_name = 'historico'

    def get_queryset(self):
        # A lógica de filtragem da view de função foi movida para este método.
        celula_id = self.request.GET.get('celula_id')
        data_reuniao_str = self.request.GET.get('data_reuniao')

        frequencias_qs = Frequencia.objects.all()

        if celula_id:
            frequencias_qs = frequencias_qs.filter(reuniao__celula__pk=celula_id)
        
        if data_reuniao_str:
            try:
                selected_data_reuniao = datetime.strptime(data_reuniao_str, '%Y-%m-%d').date()
                frequencias_qs = frequencias_qs.filter(reuniao__data_reuniao=selected_data_reuniao)
            except ValueError:
                messages.error(self.request, 'Formato de data inválido. Use AAAA-MM-DD.')

        # Agrupar frequências por membro
        membros_com_frequencia = Membro.objects.filter(frequencia__in=frequencias_qs).distinct().order_by('nome_completo')
        
        historico = []
        for membro in membros_com_frequencia:
            frequencias_membro = frequencias_qs.filter(membro=membro).order_by('reuniao__data_reuniao', 'reuniao__hora_reuniao')
            if frequencias_membro.exists():
                historico.append({
                    'membro': membro,
                    'frequencias': frequencias_membro
                })
        return historico

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        celula_id = self.request.GET.get('celula_id')
        data_reuniao_str = self.request.GET.get('data_reuniao')

        # Obter todas as células e datas de reunião para os filtros do formulário
        context['celulas'] = Celula.objects.all().order_by('nome')
        context['datas_reuniao_disponiveis'] = Reuniao.objects.values_list('data_reuniao', flat=True).distinct().order_by('-data_reuniao')
        context['selected_celula_id'] = int(celula_id) if celula_id else ''
        context['selected_data_reuniao'] = data_reuniao_str
        context['titulo_pagina'] = 'Histórico de Frequência'
        return context

# A view de seleção de reunião para frequência continua sendo uma função, pois lida com
# a lógica de redirecionamento, que é mais fácil de gerenciar assim.
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

# A view de registro de frequência também continua como uma função devido à sua lógica
# complexa de criação de múltiplos objetos Frequencia através de um formulário personalizado.
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

# A view de PDF também permanece como função, pois lida com um tipo de resposta
# não-padrão (um arquivo PDF).
def gerar_pdf_historico_frequencia(request):
    celula_id = request.GET.get('celula_id')
    data_reuniao_str = request.GET.get('data_reuniao')
    
    celulas_para_relatorio = []
    reunioes_qs = Reuniao.objects.all()

    if data_reuniao_str:
        try:
            selected_data_reuniao = datetime.strptime(data_reuniao_str, '%Y-%m-%d').date()
            reunioes_qs = reunioes_qs.filter(data_reuniao=selected_data_reuniao)
        except ValueError:
            pass 

    if celula_id:
        try:
            celula_selecionada = get_object_or_404(Celula, pk=celula_id)
            reunioes_qs = reunioes_qs.filter(celula=celula_selecionada)
            celulas_para_relatorio.append(celula_selecionada)
        except Http404:
            celulas_para_relatorio = [] 
    else:
        celulas_para_relatorio = Celula.objects.filter(reunioes__in=reunioes_qs).distinct().order_by('nome')

    celulas_com_frequencia = []
    for celula in celulas_para_relatorio:
        membros_da_celula = Membro.objects.filter(
            celula=celula,
            frequencia__isnull=False
        ).distinct().order_by('nome_completo')
        
        membros_com_frequencia_na_celula = []
        for membro in membros_da_celula:
            frequencias_membro = Frequencia.objects.filter(
                membro=membro,
                reuniao__in=reunioes_qs.filter(celula=celula)
            ).order_by('reuniao__data_reuniao', 'reuniao__hora_reuniao')
            if frequencias_membro.exists():
                membros_com_frequencia_na_celula.append({
                    'membro': membro,
                    'frequencias': frequencias_membro
                })
        
        if membros_com_frequencia_na_celula:
            celulas_com_frequencia.append({
                'celula': celula,
                'membros_da_celula': membros_com_frequencia_na_celula
            })

    titulo_documento = 'Relatório de Histórico de Frequência'
    if celula_id and celulas_para_relatorio:
        titulo_documento += f' da Célula: {celulas_para_relatorio[0].nome}'
    if data_reuniao_str:
        try:
            selected_data_reuniao_obj = datetime.strptime(data_reuniao_str, '%Y-%m-%d').date()
            titulo_documento += f' em {selected_data_reuniao_obj.strftime("%d/%m/%Y")}'
        except ValueError:
            pass

    context = {
        'celulas_com_frequencia': celulas_com_frequencia,
        'titulo_documento': titulo_documento,
        'selected_data_reuniao': data_reuniao_str
    }

    html_string = render_to_string('membros/historico_frequencia_pdf.html', context)
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historico_frequencia.pdf"'
    return response

def home_sistema(request):
    context = {
        'titulo_pagina': 'Bem-vindo IEQ CRUVIANA'
    }
    return render(request, 'membros/home_sistema.html', context)

def gestao_view(request):
    context = {
        'titulo_pagina': 'Painel de Gestão'
    }
    return render(request, 'membros/gestao_panel.html', context)
