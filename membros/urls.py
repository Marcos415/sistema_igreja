from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta linha abaixo é a "mágica" para não precisar digitar /gestao/ toda vez
    path('', lambda request: redirect('membros:home_sistema'), name='root_redirect'),
    
    # Aqui é onde você já colocou o 'gestao/' e está funcionando
    path('gestao/', include('membros.urls')),
]