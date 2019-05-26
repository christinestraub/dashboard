# Simple Dashboard with Celery

## Celery

Celery[http://docs.celeryproject.org]

```
celery -A server.jobs worker --pool=eventlet --loglevel=info
```

## Flower
Flower[https://flower.readthedocs.io/en/latest/]

```
flower -A server.jobs --port=5555
```

https://github.com/celery/celery/issues/4178
