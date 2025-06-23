from celery import shared_task


@shared_task
def log_event_task(data):
    print("Received a task")
    print(data)
    return "Success!"
