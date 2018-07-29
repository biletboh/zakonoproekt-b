from .base import *

DEBUG = False

# Sentry logs configuration
INSTALLED_APPS += ['raven.contrib.django.raven_compat',]
RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_DSN', 'default'),
}

# Security configuration
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
