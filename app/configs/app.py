import json
import os


if 'SERVER_ENV' in os.environ and os.environ['SERVER_ENV'] == 'production':
    with open("config.json", 'r') as f:
        config = json.load(f)
    NAME = config['app']['name']


else:
    with open("config.dev.json", 'r') as f:
        config = json.load(f)
    NAME = config['app']['name']
