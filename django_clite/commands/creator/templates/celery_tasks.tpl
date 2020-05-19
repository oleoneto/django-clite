from celery import shared_task


@shared_task
def my_{{ project }}_task(data=None):
    # This is a sample celery task
    pass
