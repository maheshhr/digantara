from rest_framework import mixins, status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from job.serializers import JobSerializer
from job.models import Job
from django.core.mail import EmailMessage
class CreateJobView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        post_data = request.data
        try:
            job_obj = Job()
            job_obj.name = post_data.get('name')
            job_obj.description = post_data.get('description')
            job_obj.cron_schedule = post_data.get('cron_schedule')
            job_obj.last_run = post_data.get('last_run')
            job_obj.next_run = post_data.get('next_run')
            job_obj.is_active = post_data.get('is_active')
            job_obj.save()

            return Response({'status': status.HTTP_201_CREATED, 'message': 'Created successfully.'})

        except Exception as err:
            return Response({'status': status.HTTP_205_RESET_CONTENT, 'message': f'An {err} is occurred.'})


class UpdateJobView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def find_job_object(self, pk):
        obj = self.queryset.filter(id=pk).first()
        if obj is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data found.'})
        else:
            return obj

    def put(self, request, *args, **kwargs):
        post_data = request.data
        try:
            job_id = post_data.get('job_id')
            job_obj = self.find_job_object(job_id)
            job_obj.name = post_data.get('name')
            job_obj.description = post_data.get('description')
            job_obj.cron_schedule = post_data.get('cron_schedule')
            job_obj.last_run = post_data.get('last_run')
            job_obj.next_run = post_data.get('next_run')
            job_obj.is_active = post_data.get('is_active')
            job_obj.save()
            return Response({'status': status.HTTP_200_OK, 'message': 'Updated successfully.'})
        except Exception as e:
            return Response({'status': status.HTTP_205_RESET_CONTENT, 'message': f'An error{e}'})

class DeleteJobView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def find_job_object(self, pk):
        obj = self.queryset.filter(id=pk).first()
        if obj is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data found.'})
        else:
            return obj

    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('id')
        job_obj = self.find_job_object(job_id)
        job_obj.delete()
        return Response({'status': status.HTTP_200_OK, 'message': 'Deleted successfully.'})

class ListJobView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(is_active=True)
        paginator = PageNumberPagination()
        paginator.page_size = 25
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = JobSerializer(result_page, many=True)
        return Response({'status': status.HTTP_200_OK, 'results': serializer.data})

class DetailJobView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def find_job_object(self, pk):
        obj = self.queryset.filter(id=pk).first()
        if obj is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data found.'})
        else:
            return obj

    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('id')
        job_obj = self.find_job_object(job_id)
        serializer = JobSerializer(job_obj)
        return Response({'status': status.HTTP_200_OK, 'results': serializer.data})



def send_html_email(user_email, job_name):
    subject = 'Job notification'
    plain_message = f'Hello user the job {job_name} is executed.'
    html_message = '<p>Thank you please login to your account to see the job details.</p>'
    email_from = 'jobs@gmail.com'
    recipient_list = [user_email]

    email = EmailMessage(subject, plain_message, email_from, recipient_list)
    email.content_subtype = 'html'  # Content subtype to HTML
    email.send()
