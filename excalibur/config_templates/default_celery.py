from .. import configuration as conf

broker_url = conf.get("celery", "BROKER_URL")

DEFAULT_CELERY_CONFIG = {
    "broker_url": broker_url,
    "worker_prefetch_multiplier": 1,
    "task_acks_late": True,
    "task_create_missing_queues": True,
    "task_default_queue": conf.get("celery", "DEFAULT_QUEUE"),
    "worker_concurrency": int(conf.get("celery", "WORKER_CONCURRENCY")),
}
