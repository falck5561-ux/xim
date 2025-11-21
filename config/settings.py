"""
Django settings for config project.
"""

from pathlib import Path
import os
import dj_database_url
import cloudinary # <--- IMPORTANTE: Necesario para la configuración de video
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b9!h(wl!abva$&62a1%ry%vxna5^^r*u13i-vj)r&#_(==$m&7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CORRECCIÓN 1: Permitir que Render entre a la página
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # --- 1. CLOUDINARY (Orden correcto) ---
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    # --------------------------------------------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'historia',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- Whitenoise aquí
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# CORRECCIÓN 2: Configuración Híbrida (Supabase en la nube, SQLite en tu PC)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

# CORRECCIÓN 3: Hora de México.
TIME_ZONE = 'America/Mexico_City' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# CORRECCIÓN 4: Whitenoise
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURACIÓN DE ARCHIVOS MULTIMEDIA ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- 2. CONFIGURACIÓN DE CLOUDINARY (Para guardar fotos y videos) ---

# Configuración de almacenamiento (Storage)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dd8x5gurg',
    'API_KEY': '939939232259447',
    'API_SECRET': 'E0awkZBKCn2XiJoubUc6sJp333Q',
    'SECURE_URL_PREFIX': 'https://' # Importante para evitar errores de seguridad
}

# Instrucción para que Django use Cloudinary al subir archivos
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- CONFIGURACIÓN DE LA LIBRERÍA NATIVA (ESTO ARREGLA EL ERROR DE VIDEO) ---
cloudinary.config( 
  cloud_name = "dd8x5gurg", 
  api_key = "939939232259447", 
  api_secret = "E0awkZBKCn2XiJoubUc6sJp333Q",
  secure = True
)