from django.urls import path
from .views import *
app_name="companyapp"

urlpatterns=[
    path('all/jobs/', AllJobs.as_view(), name='all-jobs'),# list all posted jobs and post new one
    path('all/jobs/<int:pk>/', AllJobs.as_view(), name='all-jobs'), # updated existing jobs details
    path('password/reset/', PasswordReset.as_view(), name='password-reset'),
    path('all/application/', AllJobsApplication.as_view(), name='all-application'),# list all job applications
    path('all/application/<int:pk>/', AllJobsApplication.as_view(), name='all-applications'),# update applications status
]