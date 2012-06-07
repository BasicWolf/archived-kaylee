from kaylee import settings as kl_settings

# Additional locations of static files
STATICFILES_DIRS = (
    kl_settings.FRONTEND_STATIC_DIR,
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_DIRS = (
    kl_settings.FRONTEND_TEMPLATES_DIR,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kaylee.frontends.django_frontend'
)

ROOT_URLCONF = 'kl_django.urls'

WSGI_APPLICATION = 'kl_django.wsgi.application'

#----------------------------------------------------------------------

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Helsinki'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

USE_L10N = True

USE_TZ = True

SECRET_KEY = 'zhp#c4!65gua-s*js!)ch(eh2$o082+$lw9q=fk)c^#g-t4mva'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
