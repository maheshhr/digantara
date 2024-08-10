from django.urls import path
from job.views import (CreateJobView,UpdateJobView,DeleteJobView,ListJobView, DetailJobView,)
urlpatterns = [
    path('create/', CreateJobView.as_view(), name='create'),
    path('update/', UpdateJobView.as_view(), name='update'),
    path('delete/<int:id>/', DeleteJobView.as_view(), name='delete'),
    path('list/', ListJobView.as_view(), name='list'),
    path('detail/<int:id>/', DetailJobView.as_view(), name='detail'),
]