from vocabventure.celery import shared_task

@shared_task
def update_user_streaks():
    print("Updating user streaks...")