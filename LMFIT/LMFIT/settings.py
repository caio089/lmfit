from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "lmfit.onrender.com", ".onrender.com"]

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # seus apps
    "loja",
]

# Middleware
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "loja.middleware.EnsureAdminUserMiddleware",  # Garantir que admin existe
]

ROOT_URLCONF = "LMFIT.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LMFIT.wsgi.application"

# Banco de dados
if os.getenv("RENDER") == "TRUE" or (os.getenv("DATABASE_URL") and not os.getenv("DATABASE_URL").startswith("sqlite")):
    # Produção - usar PostgreSQL do Supabase
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Desenvolvimento local - usar SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# Internacionalização
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Arquivos de mídia
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Supabase (para API/storage)
# IMPORTANTE: Configure as variáveis de ambiente no Render ou arquivo .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Chave anônima (anon key)
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Chave de serviço (service_role key)
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "roupas")

# Validação das variáveis obrigatórias
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL não está definida nas variáveis de ambiente")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY não está definida nas variáveis de ambiente")
if not SUPABASE_SERVICE_KEY:
    raise ValueError("SUPABASE_SERVICE_KEY não está definida nas variáveis de ambiente")

# Debug das variáveis do Supabase (apenas em desenvolvimento)
if DEBUG:
    print(f"🔍 DEBUG SUPABASE:")
    print(f"   SUPABASE_URL: {SUPABASE_URL[:50]}..." if SUPABASE_URL else "   SUPABASE_URL: NÃO DEFINIDA")
    print(f"   SUPABASE_KEY: {'DEFINIDA' if SUPABASE_KEY else 'NÃO DEFINIDA'}")
    print(f"   SUPABASE_SERVICE_KEY: {'DEFINIDA' if SUPABASE_SERVICE_KEY else 'NÃO DEFINIDA'}")
    print(f"   SUPABASE_STORAGE_BUCKET: {SUPABASE_STORAGE_BUCKET}")

# Login
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/painel/"
LOGOUT_REDIRECT_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {"django": {"handlers": ["console"], "level": "INFO", "propagate": False}},
}

# Segurança extra em produção
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

