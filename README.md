
# Redis connection leak with celery/django/gevent

Reproduces celery issue at
https://github.com/celery/celery/issues/6819 using gevented django web server and redis cache.

Some more good discussion here:
 https://github.com/redis/redis-py/issues/1495

## Setup

1. `pip install -r requirements.txt`
2. Run server:
    `gunicorn -k gevent redis_leak.wsgi:application`
3. Run celery:
    `celery -A redis_leak.celery worker --pool gevent --loglevel=info`

## Make a ton of requests

First run `python.py load.py` - this will make requests to our django webserver to a view that executes and waits for the result from a debug celery task. This will make these requests in a tight loop until you kill the process. Keep this running while you monitor your redis connections

## Meaure connections

- `redis-cli info Clients` shows "connected_clients"

- `while /bin/true; do date --iso=seconds; redis-cli -c -h localhost -p 6379 CLIENT LIST | wc -l; sleep 2; done;`

You'll hopefully find these connections are growing as your requests pile up. You'll also find these connections remain after killing your request loop. If you kill your gunicorn+gevent webserver they all go away.
