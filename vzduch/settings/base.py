"""
Django settings for vzduch project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ou9#c2t=h^2$a0wbnqcui8+c5kwoovl9fy(-f3vub1a*gp4+t('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "airMonitor",
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

ROOT_URLCONF = 'vzduch.urls'

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

WSGI_APPLICATION = 'vzduch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'airMonitor/statics/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'airMonitor/logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

POLLUTANTS_LIMIT = {
    "pm10": {
        1: 20,
        2: 40,
        3: 100,
        4: 180,
    },
    "pm2_5": {
        1: 14,
        2: 25,
        3: 70,
        4: 140
    },
    "so2": {
        1: 25,
        2: 50,
        3: 350,
        4: 500
    },
    "no2": {
        1: 20,
        2: 40,
        3: 200,
        4: 400
    },
    "co": {
        1: 1000,
        2: 2000,
        3: 10000,
        4: 30000
    },
    "o3": {
        1: 33,
        2: 65,
        3: 180,
        4: 240
    }
}

POLLUTANTS = ["pm10", "pm2_5", "so2", "no2", "co", "o3"]

COLORS = {
    0: ["grey", "#efefef"],
    1: ["green", "#00b050"],
    2: ["light green", "#92d050"],
    3: ["yellow", "#ffff00"],
    4: ["orange", "#ffc000"],
    5: ["red", "#ff0000"]
}

DATA_COLORS = {
    "red": "rgb(255, 99, 132)",
    "orange": "rgb(255, 159, 64)",
    "yellow": "rgb(255, 205, 86)",
    "green": "rgb(75, 192, 192)",
    "blue": "rgb(54, 162, 235)",
    "purple": "rgb(153, 102, 255)",
    "light green": "rgb(153, 255, 204)",
    "cyan": "rgb(0, 255, 255)"
}

RETRY_NUMBER = 4
