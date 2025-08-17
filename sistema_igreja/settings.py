"""
Configuracoes do Django para o projeto sistema_igreja.

Gerado por 'django-admin startproject' usando Django 5.0.

Para mais informacoes, veja
https://docs.djangoproject.com/en/5.0/topics/settings/

Para a lista completa de configuracoes, veja
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url

# O BASE_DIR e o diretorio raiz do projeto Django.
BASE_DIR = Path(__file__).resolve().parent.parent

# A SECRET_KEY e uma chave de seguranca para o seu projeto.
# Em producao, e crucial que ela seja lida de uma variavel de ambiente.
# Isso evita que a chave seja exposta no codigo-fonte.
# O Render.com permite que voce adicione variaveis de ambiente facilmente.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-m&l%w-y^o@#=7(y1q&!m+g9*^71y0c_k(i&6k8!&2c62)h3r1-')

# A configuracao DEBUG deve ser False em producao.
# Lemos a variavel de ambiente 'RENDER' para saber se estamos em producao.
# A variavel 'RENDER' e definida automaticamente pelo Render.com.
DEBUG = 'RENDER' not in os.environ

# O ALLOWED_HOSTS define quais dominios podem acessar sua aplicacao.
# E importante adicionar o dominio do Render.
# Lemos a variavel de ambiente 'RENDER_EXTERNAL_HOSTNAME' para obter o dominio.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# INSTALLED_APPS define os aplicativos Django ativados neste projeto.
# Se a pasta 'membros' estiver na raiz, a linha deve ser 'membros'.
# Se a pasta 'membros' estiver dentro da pasta 'sistema_igreja',
# a linha deve ser 'sistema_igreja.membros'.
# Verifique a sua estrutura de pastas localmente.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'membros', # OU 'sistema_igreja.membros' dependendo da sua estrutura
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistema_igreja.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema_igreja.wsgi.application'


# Configuracao do Banco de Dados.
# Por padrao, usamos o SQLite3 para desenvolvimento.
# Para producao no Render, e recomendado usar um banco de dados externo
# como o PostgreSQL, configurado via variavel de ambiente.
# A biblioteca dj_database_url facilita essa configuracao.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# A linha abaixo ira sobrescrever a configuracao do banco de dados para PostgreSQL
# se a variavel de ambiente DATABASE_URL for encontrada (como no Render).
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Boa_Vista'

USE_I18N = True

USE_TZ = True

# Configuracoes para arquivos estaticos.
# STATIC_URL e o caminho para acessar os arquivos estaticos no navegador.
STATIC_URL = 'static/'

# STATICFILES_DIRS e o caminho para as pastas onde voce guarda os arquivos estaticos
# durante o desenvolvimento.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# STATIC_ROOT e o caminho onde o Django ira coletar todos os arquivos estaticos
# para o deploy. Esta e a variavel que estava faltando e causava o erro.
# O comando `collectstatic` ira usar esta pasta para juntar todos os arquivos.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'