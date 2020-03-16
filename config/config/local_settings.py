from .settings import *
import os 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite333'),
    }
}

DEBUG = False

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
    ALLOWED_HOSTS = ["*", "0.0.0.0"]