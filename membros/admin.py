from django.contrib import admin
from .models import Membro, Celula, Reuniao, Frequencia

# Registra o modelo Membro no admin
@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista de membros no admin
    list_display = ('nome_completo', 'celula', 'data_adesao', 'telefone', 'email')
    # Campos pelos quais você pode pesquisar
    search_fields = ('nome_completo', 'celula__nome', 'telefone', 'email')
    # Campos pelos quais você pode filtrar na barra lateral direita
    list_filter = ('celula', 'data_adesao') # Removido 'sexo'
    # Campos que se tornam links para a página de edição
    list_display_links = ('nome_completo',)
    # Campos editáveis diretamente na lista
    list_editable = ('celula', 'telefone', 'email')


# Registra o modelo Celula no admin
@admin.register(Celula)
class CelulaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'lider', 'descricao')
    search_fields = ('nome', 'lider')
    list_filter = ('lider',)


# Registra o modelo Reuniao no admin
@admin.register(Reuniao)
class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ('tema', 'data_reuniao', 'hora_reuniao', 'celula')
    search_fields = ('tema', 'celula__nome')
    list_filter = ('celula', 'data_reuniao')
    date_hierarchy = 'data_reuniao' # Adiciona uma navegação por data


# Registra o modelo Frequencia no admin
@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('reuniao', 'membro', 'presente', 'observacao')
    search_fields = ('reuniao__tema', 'membro__nome_completo', 'reuniao__celula__nome')
    list_filter = ('reuniao__celula', 'reuniao__data_reuniao', 'presente')
    # Permite editar o status de presença diretamente na lista
    list_editable = ('presente',)
