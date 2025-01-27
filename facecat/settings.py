

from pathlib import Path
from datetime import timedelta
import os
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent




DEFAULT_FILE_STORAGE = 'facecat.storages.backblaze_b2_storage.BackblazeB2Storage'

# Remplacez ces valeurs par vos informations
B2_KEY_ID = '30344dba5bed'  # Votre Key ID
B2_APPLICATION_KEY = '003730a9961ada6beabc45fb330ffebfc82f767e1a'  # Votre Application Key
B2_BUCKET_NAME = 'facecat'  # Remplacez par le nom de votre bucket

MEDIA_URL = 'https://f003.backblazeb2.com/file/{}/'.format(B2_BUCKET_NAME)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#o3e-)cxh9c!1x$!)i^_7m4h7=z8@qk(dl*%#5cpmz2c95o9ae'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'yourdomain.com', 'your-angular-dev-server-host']

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'x-requested-with',
    'accept',
    'origin',
    'cache-control',  # Ajoutez cet en-tête ici
    'x-custom-header',  # Si vous utilisez des en-têtes personnalisés

]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:4200$",  # Permet les requêtes depuis http://localhost:4200
]

CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cat',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    'storages',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'facecat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'facecat.wsgi.application'

ASGI_APPLICATION = 'facecat.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Log to stdout
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'cat.CustomUser'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Moteur PostgreSQL
        'NAME': 'Catbook',    # Nom de votre base de données
        'USER': 'postgres',                # Nom d'utilisateur de la base de données
        'PASSWORD': 'Jamesbond007colibri+',           # Mot de passe de la base de données
        'HOST': 'localhost',                        # Adresse IP du serveur de base de données. Par défaut : 'localhost'
        'PORT': '5432',                             # Port de la base de données. Par défaut : '5432'
    }
}

CORS_ALLOW_ALL_ORIGINS = False  # Autoriser toutes les origines (utilisé uniquement en développement)
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:4200",
    "http://127.0.0.1:9000",
    "http://127.0.0.1:4200",
     'https://f003.backblazeb2.com',


]
CORS_ALLOW_CREDENTIALS = True  # Autoriser l'envoi de cookies et d'informations d'authentification



SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Utilisation d'une session en base de données
SESSION_COOKIE_SECURE = False  # Assurez-vous d'utiliser HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session expirée uniquement à la fermeture du navigateur
SESSION_COOKIE_AGE = 1209600  # 2 semaines par défaut

# Configuration de la politique de cookie CSRF
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',

        # Ajoutez l'URL de votre frontend ici
]

# Pour simplifier le développement, ajustez ceci en fonction de vos besoins en production