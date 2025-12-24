# sistema_igreja/urls.py
from django.contrib import admin
from django.urls import path, include
# Adicione esta linha para importar as views do seu app 'membros'
# Certifique-se que 'membros' é o nome do seu aplicativo Django.
# Se você tiver uma view diretamente no seu urls.py principal,
# precisará importar ela ou o módulo de views correspondente.
# Dado o erro, parece que você está tentando usar views do app 'membros' diretamente aqui.
from membros import views # <--- ADICIONE ESTA LINHA!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta linha provavelmente deveria ser assim para incluir as URLs do seu app 'membros':
    path('gestao/', include('membros.urls')), # O prefixo 'gestao/' para todas as suas URLs de membros
    
    # Se você tem algumas URLs diretas aqui, elas precisam da importação 'views'
    # path('membros/listar/', views.listar_membros, name='listar_membros'), # Esta linha gerou o erro
    # Recomendo que as URLs do seu app 'membros' fiquem no 'membros/urls.py'
    # e sejam incluídas aqui com 'include('membros.urls')' como na linha acima.
    # Se a linha acima (path('gestao/', include('membros.urls'))) já existe e está correta,
    # você pode remover a linha problematica: path('membros/listar/', views.listar_membros, name='listar_membros'),
    # pois ela já estaria sendo tratada dentro de 'membros.urls' via 'include'.
]