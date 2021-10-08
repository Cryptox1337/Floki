import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")

DB_URL = (
    f"mysql://{os.environ.get('DB_USER')}"
    f":{os.environ.get('DB_PASSWORD')}"
    f"@{os.environ.get('DB_HOST')}:3306/{os.environ.get('DB_NAME')}"
)

TORTOISE_ORM = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': os.environ.get('DB_HOST'),
                'port': '3306',
                'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_PASSWORD'),
                'database': os.environ.get('DB_NAME'),
            }
        }
    },
    'apps': {
        'my_app': {
            "models": ["models", "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'UTC'
}