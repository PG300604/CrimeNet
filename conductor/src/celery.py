"""
Celery initialization
"""
from datetime import timedelta
from celery import Celery
from .config import config

celery = Celery(
    "CrimeNetAPI",
    broker=config["CELERY_BROKER_URL"],
    backend=config["CELERY_RESULT_BACKEND"],
    include=["conductor.src.tasks.celery_tasks"],
    task_serizalizer="pickle",
    task_compression="bzip2",
    result_serializer="pickle",
    result_compression="bzip2",
    result_expires=timedelta(minutes=config["CELERY_PERSIST_RESULT"])
)

celery.conf.update(config)
