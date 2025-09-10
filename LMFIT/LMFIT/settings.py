from pathlib import Path
import os
import dj_database_url  # precisa estar no requirements.txt

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------
# Segurança
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")  # nunca usar em produção
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]  # depois pode restringir para o domínio do Render

# Configuração para Render
if os.getenv("RENDER"):
    ALLOWED_HOSTS = ["*"]

# -------------------------------------------------
# Aplicativos
# -------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # seus apps
    'LMFIT',
    'loja',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise precisa vir logo após SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'LMFIT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # se quiser usar templates globais, pode adicionar BASE_DIR / "templates"
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

# -------------------------------------------------
# Banco de dados
# -------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# Configuração específica para Render
if os.getenv("RENDER"):
    # No Render, sempre usar PostgreSQL se DATABASE_URL estiver disponível
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.strip():
        DATABASES = {
            "default": dj_database_url.config(
                default=database_url,
                conn_max_age=600,
            )
        }
        print(f"✅ Usando PostgreSQL no Render: {database_url[:50]}...")
    else:
        print("⚠️ DATABASE_URL não encontrado no Render, usando SQLite")
        # Fallback para SQLite se DATABASE_URL não estiver disponível
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
else:
    print("🏠 Usando SQLite local")

# -------------------------------------------------
# Validação de senha
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {"NAME": 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {"NAME": 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {"NAME": 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------
# Internacionalização
# -------------------------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Arquivos estáticos e mídia
# -------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------------------------
# Configurações padrão
# -------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
