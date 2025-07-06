import os

class Config:
    CLIENT_ID = os.getenv("E5_CLIENT_ID")
    CLIENT_SECRET = os.getenv("E5_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("E5_REFRESH_TOKEN")
    REDIRECT_URI = "http://localhost:53682/"
    TIME_DELAY = int(os.getenv("E5_TIME_DELAY", 3))

```
LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'event-log.txt',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'uvicorn.error': {
            'level': 'WARNING',
            'handlers': ['file_handler', 'stream_handler']
        },
        'https': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
    }
}
```
