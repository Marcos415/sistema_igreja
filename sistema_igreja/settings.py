"""
Configurações do Django para o projeto sistema_igreja.
"""

import os
from pathlib import Path
import dj_database_url

# O BASE_DIR e o diretório raiz do projeto Django.
BASE_DIR = Path(__file__).resolve().parent.parent

# A SECRET_KEY é uma chave de segurança para o seu projeto.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-m&l%w-y^o@#=7(y1q&!m+g9*^71y0c_k(i&6k8!&2c62)h3r1-')

# A configuração DEBUG deve ser False em produção.
DEBUG = 'RENDER' not in os.environ

# O ALLOWED_HOSTS define quais domínios podem acessar sua aplicação.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# INSTALLED_APPS define os aplicativos Django ativados neste projeto.
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# Configurações para arquivos estáticos.
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ESTA LINHA DEVE ESTAR AQUI!
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
