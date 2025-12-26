from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect # Importação necessária para o redirecionamento

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inclui todas as rotas do seu app membros sob o prefixo /gestao/
    path('gestao/', include('membros.urls')), 
    
    # REDIRECIONAMENTO: Faz com que a página inicial (vazia) vá direto para a gestão
    # Isso corrige o botão "Ver o site" do painel administrativo
    path('', lambda request: redirect('gestao/', permanent=True)),
]