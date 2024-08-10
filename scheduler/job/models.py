from django.db import models

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cron_schedule = models.CharField(max_length=100)  # Example: '0 0 * * MON'
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
