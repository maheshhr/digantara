from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .models import Job
from .tasks import execute_job

@receiver(post_save, sender=Job)
def schedule_job(sender, instance, **kwargs):
    # Schedule for every Monday at 10:00 AM
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='10',
        day_of_week='1',  # 1 corresponds to Monday
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name='Execute job every Monday',
        task='scheduler.tasks.execute_job',
        args=json.dumps([job_id]),  # Replace job_id with the actual job ID
    )
