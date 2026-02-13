from app.tasks.celery_app import celery
import time

@celery.task(name="demo.add")
def add(a: int, b: int):
    time.sleep(2)
    return a + b