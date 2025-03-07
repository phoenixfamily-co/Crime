import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=56+47c2k8yph88k#z_89w@j7-3o-1*1^48ig=g^w$u+c=rizm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DOMAIN = 'crime.phoenixfamily.co'
SITE_NAME = 'crime'
SITE_URL = "https://crime.phoenixfamily.co"

SITE_ID = 1

META_SITE_PROTOCOL = "https"
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_SCHEMAORG_PROPERTIES = True

CSRF_TRUSTED_ORIGINS = ["https://crime.phoenixfamily.co", "https://www.crime.phoenixfamily.co"]

ALLOWED_HOSTS = [
    'localhost',
    'crime.phoenixfamily.co',
    'www.crime.phoenixfamily.co'
]

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',  # برای ساخت Sitemap
    'django.contrib.humanize',  # برای نمایش بهتر اعداد و تاریخ‌ها
    'django_user_agents',
    'rest_framework',
    'django_extensions',
    'Home',
    'Product',
    'User',
    'Cart',
    'Category',
    'Order',
    'Play',
    'Podcast',
    'About',
    'Contact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'CrimeProject.middleware.MobileOnlyMiddleware',

]

ROOT_URLCONF = 'CrimeProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'CrimeProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phoenixf_crime',  # نام دیتابیس
        'USER': 'phoenixf_crime',  # نام کاربری دیتابیس
        'PASSWORD': 's=4deM.C}9O3',  # رمز عبور دیتابیس
        'HOST': 'localhost',  # آدرس سرور MySQL (یا آدرس دلخواه)
        'PORT': '3306',  # پورت MySQL (پورت پیش‌فرض: 3306)
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

SEO = {
    'default': {
        'title': _('Phoenix Family | Board Games, Entertainment Apps & More!'),
        'description': _(
            'Discover Phoenix Family – your ultimate destination for family entertainment! From online entertainment to'
            ' entertainment apps and best board games for adults, fun awaits!'),
        'keywords': [
            _('phoenix family'),
            _('family entertainment'),
            _('entertainment online'),
            _('entertainment apps'),
            _('family board games'),
            _('board game online'),
            _('board game apps'),
            _('game apps'),
            _('best entertainment apps'),
            _('best board games for adults'),
        ],
        'robots': 'index, follow',  # یا 'noindex, nofollow' برای جلوگیری از ایندکس
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
    ('ar', _('Arabic')),
    ('tr', _('Turkish')),
    ('ru', _('Russian')),
    ('hi', _('Hindi')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    # ('zh-hans', _('Simplified Chinese')),  # چینی ماندارین ساده‌شده

]

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # مسیر پوشه‌ی locale
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = '/home/phoenixf/crime.phoenixfamily.co/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # اگر فایل استاتیکی دارید که در مسیر پروژه هستند.
]

MEDIA_ROOT = '/home/phoenixf/crime.phoenixfamily.co/media/'
MEDIA_URL = '/media/'

ROBOTS_FILE_PATH = '/home/abbaslot/public_html/robots.txt/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'User.User'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.phoenixfamily.co'
EMAIL_PORT = 465  # پورت SMTP
EMAIL_USE_TLS = False  # TLS غیرفعال است
EMAIL_USE_SSL = True  # SSL فعال است
EMAIL_HOST_USER = 'customer@phoenixfamily.co'
EMAIL_HOST_PASSWORD = 'n.Y?8&eg0$60'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
COMPANY_EMAIL = 'info@phoenixfamily.co'
