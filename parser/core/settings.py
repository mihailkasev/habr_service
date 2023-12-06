import os
from dotenv import load_dotenv

load_dotenv()

HABR = os.getenv('HABR')

REDIS = {
    'url': f'redis://{os.getenv("REDIS_HOST")}',
}
CONNECTION_LIMIT = 50
CONNECTION_PARAMS = {
    'sock_connect': 5,
    'sock_read': 15
}
