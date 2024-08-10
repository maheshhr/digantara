from celery import shared_task
from .models import Job
from datetime import datetime
from celery.schedules import crontab
from .views import send_html_email
@shared_task
def execute_job(job_id):
    job = Job.objects.get(id=job_id)
    job.last_run = datetime.now()
    # Example dummy job: sending email
    send_html_email('userone@gmail.com', job.name)
    print(f"Executing job: {job.name}")
    job.next_run = datetime.now() + crontab(schedule=job.cron_schedule).remaining_estimate(datetime.now())
    job.save()
