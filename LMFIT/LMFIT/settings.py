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
# Valores padrão para desenvolvimento local
DEFAULT_SUPABASE_URL = "https://ubasgcbrwjdbhtxandrm.supabase.co"
DEFAULT_SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViYXNnY2Jyd2pkYmh0eGFuZHJtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc3NjY2OTAsImV4cCI6MjA3MzM0MjY5MH0.jOWVQq_Yrl0LkFLj2IK2B0l1aHv2Pl5dxgne944eq5o"
DEFAULT_SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViYXNnY2Jyd2pkYmh0eGFuZHJtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Nzc2NjY5MCwiZXhwIjoyMDczMzQyNjkwfQ.ujQBq-ctCrkFtneCeZ-Li_FsE8eSg2muu0t6R74RvGw"

# Carregar variáveis do ambiente ou usar valores padrão
SUPABASE_URL = os.getenv("SUPABASE_URL", DEFAULT_SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY", DEFAULT_SUPABASE_KEY)
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", DEFAULT_SUPABASE_SERVICE_KEY)
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "roupas")

# Debug das variáveis do Supabase
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

