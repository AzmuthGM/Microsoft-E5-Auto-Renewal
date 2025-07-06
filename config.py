import os

class Config:
CLIENT\_ID = os.getenv("E5\_CLIENT\_ID")
CLIENT\_SECRET = os.getenv("E5\_CLIENT\_SECRET")
REFRESH\_TOKEN = os.getenv("E5\_REFRESH\_TOKEN")
REDIRECT\_URI = "[http://localhost:53682/](http://localhost:53682/)"
TIME\_DELAY = int(os.getenv("E5\_TIME\_DELAY", 3))

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
