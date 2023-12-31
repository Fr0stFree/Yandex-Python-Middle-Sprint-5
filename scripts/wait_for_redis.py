import os
import time

from dotenv import load_dotenv
from redis import Redis

load_dotenv()

if __name__ == '__main__':
    redis_client = Redis(host=f'{os.getenv("REDIS_HOST")}')
    while True:
        if redis_client.ping():
            print('Success connect Redis')
            break
        time.sleep(1)