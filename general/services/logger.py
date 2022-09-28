import logging

from ..settings import settings

logging.basicConfig(
    format='%(asctime)s, %(msecs)d %(name)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=settings.LOGGING_LEVEL,
    **{'handlers': [
        logging.FileHandler(settings.LOGGING_FILE_PATH, mode='a+'),
        logging.StreamHandler()
    ]
    } if settings.LOGGING_FILE_PATH is not None else {}
)

BROWSER_LOGGER = logging.getLogger('BROWSER_LOGGER')
