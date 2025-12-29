# membros/admin.py
from django.contrib import admin
from .models import Membro, Celula, Reuniao, Frequencia

# Classe Admin para Membro
@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de membros no painel de admin
    list_display = (
        'nome_completo', 
        'celula', 
        'data_adesao', 
        'sexo', # Adicionei 'sexo' aqui, assumindo que você o adicionou ao modelo
        # Removi 'ativo', 'telefone', 'email' pois não estão no seu models.py
    )
    # Campos que podem ser usados para filtrar a lista de membros
    list_filter = (
        'celula', 
        'sexo', # Adicionei 'sexo' aqui para filtragem
        'data_adesao',
        # Removi 'ativo' pois não está no seu models.py
    )
    # Campos pelos quais você pode pesquisar membros
    search_fields = ('nome_completo', 'celula__nome')
    # Campos que se tornam links para a página de edição
    list_display_links = ('nome_completo',)
    # Campos que podem ser editados diretamente na lista
    list_editable = ('celula',)


# Classe Admin para Célula
@admin.register(Celula)
class CelulaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'total_membros_celula')
    search_fields = ('nome', 'lider')
    list_filter = ('lider',)

    def total_membros_celula(self, obj):
        # Um método personalizado para contar membros por célula
        return obj.membros.count()
    total_membros_celula.short_description = 'Total de Membros' # Nome da coluna


# Classe Admin para Reunião
@admin.register(Reuniao)
class ReuniaoAdmin(admin.ModelAdmin):
    list_display = (
        'celula', 
        'data_reuniao', 
        'tema',
        # Removi 'observacoes' pois não está no seu models.py
    )
    list_filter = ('celula', 'data_reuniao')
    search_fields = ('celula__nome', 'tema')
    # Permite navegar por data
    date_hierarchy = 'data_reuniao' # Corrigido para 'data_reuniao'


# Classe Admin para Frequência
@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = (
        'reuniao', 
        'membro', 
        'presente', 
        'get_data_reuniao' # Método para exibir a data da reunião
        # Removi 'data_registro' pois não está no seu models.py
    )
    list_filter = ('reuniao__celula', 'presente', 'reuniao__data_reuniao') # Filtra por célula e data da reunião
    search_fields = ('membro__nome_completo', 'reuniao__celula__nome', 'reuniao__tema')
    
    # Adicionando um método para exibir a data da reunião no list_display da Frequência
    def get_data_reuniao(self, obj):
        return obj.reuniao.data_reuniao.strftime('%d/%m/%Y')
    get_data_reuniao.short_description = 'Data da Reunião'

    # date_hierarchy para Frequencia deve ser baseado em um campo DateField ou DateTimeField.
    # Como 'data_registro' não existe, usamos 'reuniao__data_reuniao' que é do modelo Reuniao.
    date_hierarchy = 'reuniao__data_reuniao'