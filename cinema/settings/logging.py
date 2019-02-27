import logging.config
import os

BASE_DIR_LOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR_LOG, 'cinema.log'),
            'maxBytes': 1024 * 1024 * 1,  # 1MB
            'backupCount': 10,
            'formatter': 'simple'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(funcName)s|%(lineno)d|%(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s|%(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
logging.config.dictConfig(LOGGING)