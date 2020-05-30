"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!p1ai_b373g3bmz-**m@%h9+0_8xm7*41etdbi+t266-mogm08'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only



# Application definition

INSTALLED_APPS = [
       # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My apps
    'personal',
    'account',
    'blog',
    'carts',
    'products',
    'orders',
    'inquiry',
    'users',
    'newsletter',
    'membership',

    'crispy_forms',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    # 'drfpasswordless',
    'rest_registration',


 
]

AUTH_USER_MODEL = 'account.Account'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BRAINTREE_PUBLIC = "qn3p5n7njksw47r3"
BRAINTREE_PRIVATE = "d14ac944794c0df1c81991ecf49221ff"
BRAINTREE_MERCHANT_ID = "n84nynknvzz3j3sz"
BRAINTREE_ENVIRONEMNT = "Sandbox"
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = 'f472a1b791bc03'
EMAIL_HOST_PASSWORD = 'efe5fe413946a6'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True



SERVER_HOST = 'http://localhost:8000'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
        'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
      'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        
    ),
      'DEFAULT_PAGINATION_CLASS': 'products.pagination.ProductPagination',
      "SEARCH_PARAM" : "q"
}

JWT_AUTH = {
    "JWT_RESPONSE_PAYLOAD_HANDLER": 
            "mysite.utils.jwt_response_payload_handler",
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10000),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # 'JWT_VERIFY_EXPIRATION': False,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30000),
}



REST_REGISTRATION = {
    'SEND_RESET_PASSWORD_LINK_SERIALIZER_USE_EMAIL': True,
    'REGISTER_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_ENABLED': True,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,

    'REGISTER_EMAIL_VERIFICATION_URL': SERVER_HOST+'/accounts/verify-email/',
    # 'REGISTER_VERIFICATION_URL': 'http://localhost:8000/accounts/verify-registration/',
    'REGISTER_VERIFICATION_URL': SERVER_HOST+'/accounts-verify-registration/',

    'RESET_PASSWORD_VERIFICATION_URL': SERVER_HOST+ '/accounts-reset-password/',
    # 'SEND_RESET_PASSWORD_LINK' : 'http://localhost:8000/jpt/',
    

    'VERIFICATION_FROM_EMAIL': EMAIL_HOST_USER,
}

# AUTHENTICATION_BACKENDS = (
#     'mysite.backends.UsernameOrEmailBackend',
#     'django.contrib.auth.backends.ModelBackend' )


