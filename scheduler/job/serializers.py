from rest_framework import serializers
from job.models import Job
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'name',
            'description',
            'cron_schedule',
            'last_run',
            'next_run',
            'is_active'
        ]
