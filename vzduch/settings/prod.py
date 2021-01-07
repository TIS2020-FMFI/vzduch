from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


GUST_PATH = os.getcwd() + '/airMonitor/static/air/GUST'
VEIND_PATH = os.getcwd() + '/airMonitor/static/air/VEIND'