"""
Configurações de produção para Render + Supabase
"""
from .settings import *
import dj_database_url
import os

# Forçar DEBUG = False em produção
DEBUG = False

# Hosts permitidos
ALLOWED_HOSTS = ["lmfit.onrender.com", ".onrender.com"]

# Banco de dados usando DATABASE_URL do Render/Supabase
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,  # mantém conexões persistentes
        ssl_require=True   # exige SSL
    )
}

# Arquivos estáticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Segurança extra
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging de produção
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "loja": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Supabase (opcional, se você usar API/storage)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "roupas")
