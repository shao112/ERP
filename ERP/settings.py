"""
Django settings for ERP project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = 'http://localhost:8000'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8su&88t&mwf&_r25(qxnmnw8os58s=&7usp4ny47b*%%r(o+%l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

#方便測試URL
# PASS_TEST_FUNC=True
PASS_TEST_FUNC=False

ALLOWED_HOSTS = ["*"]


# Application definition
# 指令 python manage.py collectstatic 會把這裡使用到的靜態檔案放在底下 STATIC_ROOT 路徑

INSTALLED_APPS = [
    #託管
    "daphne",
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # APP
    'Frontend',
    'Backend',
    # 套件
    'django_cleanup',
    'background_task',
    #
    "django_extensions",
]
BACKGROUND_TASK_RUN_ASYNC = True

ASGI_APPLICATION = 'ERP.asgi.application'



DJANGO_TASKS = [
    'Backend.cron.CalculateAnnualLeaveTask',
]

IMPORT_EXPORT_USE_TRANSACTIONS = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #自訂一MIDDLEWARE
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

ROOT_URLCONF = 'ERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Frontend', 'templates').replace('\\','/'),
            os.path.join(BASE_DIR, 'Backend', 'templates').replace('\\','/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Backend.context_processors.sys_messages',  
                'Backend.context_processors.client_list',  
                'Backend.context_processors.approval_count',  
                'Backend.context_processors.pass_test_func',  

            ],
        },
    },
]

WSGI_APPLICATION = 'ERP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'ericerp',
        # 'HOST': 'localhost',
        # 'USER': 'root',
        # 'PASSWORD': '',
        # 'PORT': '3306',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

XHTML2PDF = {
    'DEFAULT_FONT': r'fonts/stsong.ttf',  # 指定你的字型文件的路徑
    # 其他 xhtml2pdf 設定...
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True



# login 

LOGIN_URL="/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
# python manage.py collectstatic 可以複製靜態檔案到此路徑
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'collect_static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_PROFILE_MODULE = 'Frontend.Employee'
