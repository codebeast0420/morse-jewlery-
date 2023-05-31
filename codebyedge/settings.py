"""
Django settings for codebyedge project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qz@rp#ze)1u=(i=+-qp!f)t4v^fz@_qx6ml2s1k*e2u!s(d)pw'


ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'customiser.codebyedge.co.uk']
CSRF_TRUSTED_ORIGINS = ['https://*.codebyedge.co.uk']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_vite',
    'staging',
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

ROOT_URLCONF = 'codebyedge.urls'

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

WSGI_APPLICATION = 'codebyedge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEBUG = True

# If use HMR or not.
DJANGO_VITE_DEV_MODE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if (DJANGO_VITE_DEV_MODE):
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / "staging" / "static"
    DJANGO_VITE_ASSETS_PATH = BASE_DIR / "staging/static" / "prod"
    STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / "staging" / "static"
    DJANGO_VITE_ASSETS_PATH = BASE_DIR
    #STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]

# Where ViteJS assets are built.

# Name of static files folder (after called python manage.py collectstatic)
# STATIC_ROOT = BASE_DIR / "collectedstatic"

# Include DJANGO_VITE_ASSETS_PATH into STATICFILES_DIRS to be copied inside
# when run command python manage.py collectstatic


# OLDDDDDD
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# DJANGO_VITE_DEV_MODE = False
# SECURITY WARNING: don't run with debug turned on in production!

# STATIC_URL = 'static/'

# if (DJANGO_VITE_DEV_MODE==True):
#    STATIC_URL = './'
# else:
#    STATIC_URL = 'static/'

# DJANGO_VITE_ASSETS_PATH = 'static/dist'
# #Name of static files folder (after called python manage.py collectstatic)
# STATIC_ROOT = BASE_DIR / "staging" / "static"


# OLDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# Where ViteJS assets are built.
# DJANGO_VITE_ASSETS_PATH = BASE_DIR / "staging" / "static" / "dist"

# DJANGO_VITE_ASSETS_PATH = STATIC_ROOT


# If use HMR or not.
# DJANGO_VITE_DEV_MODE = False


# Include DJANGO_VITE_ASSETS_PATH into STATICFILES_DIRS to be copied inside
# when run command python manage.py collectstatic
# STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]

CSRF_COOKIE_NAME = "csrftoken"

EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'customiser@codebyedge.com'
EMAIL_HOST_PASSWORD = 'HakunaMatata_88$$'
DEFAULT_FROM_EMAIL = 'customiser@codebyedge.com'

X_SHOPIFY_ACCESS_TOKEN = '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'

#EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = '1e1a8fff72a0da'
#EMAIL_HOST_PASSWORD = '78fcd4b4c03560'
#DEFAULT_FROM_EMAIL = 'customiser@codebyedge.com'