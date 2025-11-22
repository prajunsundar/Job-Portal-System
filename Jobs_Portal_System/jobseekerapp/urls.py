from django.urls import path
from .views import *
app_name="jobseekerapp"

urlpatterns=[
    path('my/profile/', MyAccount.as_view(), name='my-profile'),# to show profile and update profile
    path('password/reset/', PasswordReset.as_view(), name='password-reset'),
    path('my/application/', MyApplications.as_view(), name='my-application'),# list all applied job details
    path('job/list/', JobList.as_view(), name='jobs'),# list jobs by search and filter

]