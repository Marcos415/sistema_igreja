import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# CHAVE DE SEGURANÇA
SECRET_KEY = 'django-insecure-k!h!2a!7_b%h5v=8(0$@=w1v7d-s-j=e+j7w8q-x*y&n$p-k&'

# DEBUG (Mantenha True para testes, mude para False em produção real)
DEBUG = True

ALLOWED_HOSTS = ['gestao-igreja.onrender.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'membros',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Essencial para o Render
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Boa_Vista'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS (RESOLVE O ERRO DE BUILD) ---
STATIC_URL = 'static/'

# Local onde o Django coletará arquivos para o servidor web
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Onde o Django busca os arquivos estáticos originais no seu projeto
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuração do WhiteNoise para gerenciar cache
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'