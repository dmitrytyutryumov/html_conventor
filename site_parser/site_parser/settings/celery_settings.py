from decouple import config

__all__ = ['CELERY_BROKER_URL']

user = config('RABBITMQ_USERNAME', 'guest')
password = config('RABBITMQ_PASSWORD', 'guest')
mq_host = config('RABBITMQ_HOST', 'localhost')
mq_port = config('RABBITMQ_PASSWORD_NUMBER', 5672, cast=int)

CELERY_BROKER_URL = f'amqp://{user}:{password}@{mq_host}:{mq_port}//'
