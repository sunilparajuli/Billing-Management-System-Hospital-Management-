from . import settings_conf
# Project specific configuration
#IS_MULTI_VENDOR = True

"""
Django settings for hms project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os
import pprint

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!p1ai_b373g3bmz-**m@%h9+0_8xm7*41etdbi+t266-mogm08'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  settings_conf.GetDebug()

ALLOWED_HOSTS = ['*']

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only


#debug print usage:
#from django.conf import settings
#settings.DPRINT()
#settings.DLFPRINT() # add at begin of func

# debug print
# for 
def DPRINT(arg, ForcePrint=0):
    if(DEBUG):
        print(arg)
        pass
    if(ForcePrint != 0):
        print(arg)
    return

def dpprint(arg, ForcePrint=0):
    if(DEBUG):
        pprint.pprint(arg)
        pass
    if(ForcePrint != 0):
        pprint.pprint(arg)
    return

def dbgprint(arg, fp):
    DPRINT(arg,fp)
# call at begin of function
# To know which function is being called
# debug line and file print
# can pass func name in msg


def DLFPRINT(msg="",ForcePrint=0):
    disable_this=0 # set to 1 to disable dprint, unless forceprint is passed
    if(DEBUG):
        import inspect
        cf = inspect.currentframe()
        prevframe=inspect.currentframe().f_back
        prev_frame_info = inspect.getframeinfo(prevframe)

        #Traceback(filename='E:\\src\\products\\views.py', lineno=196,
        # function='get_queryset', code_context=['\t\tsettings.DLFPRINT()\n'], index=0)
        #print(inspect.getframeinfo(prevframe) )
        #
        #str(cf.f_back.f_lineno)
        
        msg = (
            prev_frame_info.function + ' ' + 
            'ln:' + str(prev_frame_info.lineno) + '| ' +
            prev_frame_info.filename + ' '
        )

        is_print = 0
        if(disable_this==0):
            is_print=1

        if(ForcePrint==1):
            is_print=1

        if is_print==1:
            print(msg) #comment to debug
        
        #print(arg, line, file)
        pass
    #if(ForcePrint != 0):
    #    print(arg, line, file)
    return

# Application definition

INSTALLED_APPS = [
       # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    # My apps
    
    'personal',
    'account',
    'carts',
    'products',
    'orders',
    'inquiry',
    
    'users',
    'store',
    'payment',
    'payment_esewa',
    'prescription',
    'crispy_forms',
    'slider',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_registration',
    'hms_web',
    'app_settings',
    'department',
    'doctor',
    'specializationtype',
    'nurse',
    'counter',
    'office',
    'vendor',
    'address'



 
]

AUTH_USER_MODEL = 'account.Account'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/hms_web')],
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

WSGI_APPLICATION = 'hms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

SHIPPING_PRICE = 0

DATABASES = settings_conf.GetDatabases()

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

# TIME_ZONE = 'Asia/Kathmandu'

CAN_STORE_SEE_ALL_ORDERS = False

TAX_PERCENT_DECIMAL = 0.0

IS_MULTI_VENDOR=True
CUSTOMER_STORE_MAX_DISTANCE_KM=2
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

# EMAIL_HOST = 'smtp.mailtrap.io'
# EMAIL_HOST_USER = 'a2b88d5a140f35'
# EMAIL_HOST_PASSWORD = '1eaecb0140e538'
# EMAIL_PORT = 2525
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'xunilparajuli2002@gmail.com'
EMAIL_HOST_PASSWORD = 'vnnuasmkmapqzvur'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



SERVER_HOST = settings_conf.GetServerHost()

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
        'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
      'DEFAULT_AUTHENTICATION_CLASSES': (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        
    ),
      'DEFAULT_PAGINATION_CLASS': 'products.pagination.ProductPagination',
      "SEARCH_PARAM" : "q"
}

JWT_AUTH = {
    "JWT_RESPONSE_PAYLOAD_HANDLER": 
            "hms.utils.jwt_response_payload_handler",
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10000),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # 'JWT_VERIFY_EXPIRATION': False,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30000),
}


# SPARROW_SMS_TOKEN = 'dakZyk9lTu56uck0uTZx'
# SMS_FROM = 'InfoSMS'

SPARROW_SMS_TOKEN = '3ojHG057JwjtSqn1FQUk' #'3ojHG057JwjtSqn1FQUk' ##for_sarovara
SMS_FROM = 'InfoSMS'

FCM_SERVER_KEY = 'AAAApJ4RTPk:APA91bE0xSBIy2bGRLwWTtP6tgBP0ii8rnc7DCqS8kLGqxataC7uVCS80sOzlUUEPbwIabLNmJRI_vikyUS39aRv8ok_WXmXyMwgLtWiXiYGFnxt6s1jrhP5MkJdw_R2gwTMZCuwUtCJ'



CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000"
]
LOGIN_REDIRECT_URL = '/dashboard/'

# AUTHENTICATION_BACKENDS = (
#     'hms.backends.UsernameOrEmailBackend',
# #     'django.contrib.auth.backends.ModelBackend' 
# )


