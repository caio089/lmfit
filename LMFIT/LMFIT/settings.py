from pathlib import Path
import os
import dj_database_url

# -------------------------------------------------
# Diretório base
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------
# Segurança
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key").strip()
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# -------------------------------------------------
# Banco de dados
# -------------------------------------------------
# Para usar Supabase/Postgres
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida nas variáveis de ambiente!")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# -------------------------------------------------
# Cloudinary (opcional, se usar para imagens)
# -------------------------------------------------
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL", "").strip()
if CLOUDINARY_URL:
    import cloudinary
    cloudinary.config(cloudinary_url=CLOUDINARY_URL)

# -------------------------------------------------
# Aplicações
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # seus apps
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "LMFIT.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    },
]

WSGI_APPLICATION = "LMFIT.wsgi.application"

# -------------------------------------------------
# Static e media
# -------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------------------------
# Internacionalização
# -------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Outros
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
