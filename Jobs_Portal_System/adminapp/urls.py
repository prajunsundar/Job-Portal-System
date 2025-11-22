from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
app_name="adminapp"

urlpatterns=[
    path('admin/register/',AdminRegister.as_view(),name='admin-register'),#admin registration
    path('company/register/', EmployerRegister.as_view(), name='company-register'),#employer registration
    path('jobseeker/register/', JobseekerRegister.as_view(), name='jobseeker-register'),# job seeker registration

    path('login/', LoginUser.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutUser.as_view(), name='logout_user'),

    path('password/reset/<int:pk>/',PasswordReset.as_view(),name='password-reset'),

    path('employer/profile/', AllEmployers.as_view(), name='all-employer'), # all employer with status approved
    path('employer/profile/<int:pk>/', AllEmployers.as_view(), name='update-employer-profile'), # update those employers details

    path('employer/pending/', EmployerPending.as_view(), name='employer-pending'), # to list all pending employers details
    path('employer/pending/<int:pk>/', EmployerPending.as_view(), name='employer-status'),#update employers status

    path('jobseeker/profile/', AllJobseeker.as_view(), name='all-jobseeker'),# all job seeker with status approved
    path('jobseeker/profile/<int:pk>/', AllJobseeker.as_view(), name='update-jobseeker-profile'),# update those job seeker details

    path('jobseeker/pending/', JobseekerPending.as_view(), name='jobseeker-pending'),# to list all pending job seeker details
    path('jobseeker/pending/<int:pk>/', JobseekerPending.as_view(), name='jobseeker-status'),#update employers status

    path('all/job/', AllJobs.as_view(), name='all-job'),# list all jobs with applicatio count
    path('jobs/pending/', JobsPending.as_view(), name='jobs-pending'),# list request pending jobs
    path('jobs/pending/<int:pk>/', JobsPending.as_view(), name='jobs-pendings'), # update job status


]