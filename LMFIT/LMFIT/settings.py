from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=@)s%(c6rhxjh22p1njhbcyi+r$1brb0w^ouz#!1%0*u*c-9wn'

# PRODUÇÃO
DEBUG = False
ALLOWED_HOSTS = ['lmfit.onrender.com', 'localhost', '127.0.0.1']

# Configurações de segurança para produção
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',

    # Seus apps
    'loja',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LMFIT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # pode adicionar caminhos extras se quiser
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LMFIT.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------------
# Arquivos estáticos (CSS, JS, imagens do projeto)
# --------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # pasta para produção
STATICFILES_DIRS = [BASE_DIR / 'static']  # arquivos estáticos do projeto

# Configuração do WhiteNoise para servir arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------
# Arquivos de mídia (uploads de usuários)
# --------------------------
# Configuração do Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', 'dwilcfm1z'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', 'fULjJTaWABDvFIgBHpwuiVsY1gU'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', 'J7qzlEUjQ4vwqyOtyX6PDxE9zsQL'),  # SUBSTITUA pela API_SECRET real
}

# Configurações adicionais do Cloudinary
import cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/painel/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
