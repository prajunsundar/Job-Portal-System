from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from .models import BaseProfile
from .serializer import AdminRegisterSerializer,\
    EmployerRegisterSerializer,JobseekerRegisterSerializer,LoginSerializer,\
    AdminPasswordSerializer,AdminEmployerProfileSerializer,EmployerSerializer,\
    JobseekerSerializer,AdminEmployerStatusSerializer,AdminJobSeekerStatusSerializer,AdminJobseekerProfileSerializer,\
    AdminJobSerializer,AdminJobStatusSerializer



from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .permission import IsEmployer,IsAdminUser,IsJobSeeker
from rest_framework.permissions import IsAuthenticated,AllowAny
from companyapp.models import Employer,Jobs
from jobseekerapp.models import JobSeeker,Applicant
from django.db.models import Count


class AdminRegister(APIView):
    """
    this view handles admin resgistration
    """
    def post(self,request):
        serializer=AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Admin Account Created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors})




class EmployerRegister(APIView):
    """
    this view handles employer resgistration
    """
    def post(self,request):
        serializer=EmployerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Company Registered Successfully'},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors})


class JobseekerRegister(APIView):
    """
    this view handles job seeker resgistration
    """
    def post(self,request):
        serializer=JobseekerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Job Seeker Registered Successfully'},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors})




class LoginUser(TokenObtainPairView):
    """
    this view handles role based login for admin,employer and job seeker
    """
    serializer_class = LoginSerializer

class LogoutUser(APIView):
    """
    this view handles logout for all 3 users
    """
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            refresh_token=request.data['refresh']
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'user logged out successfully'},status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class PasswordReset(APIView):
    """
    this view handles password reseting of all users by admin with password validation
    """
    permission_classes = [IsAdminUser]
    def put(self,request,pk):
        user=get_object_or_404(BaseProfile,id=pk)
        serializer=AdminPasswordSerializer(user,data=request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password reset done'},status=status.HTTP_205_RESET_CONTENT)
        return Response({'message':serializer.errors})








class AllEmployers(APIView):
    """
    this view get-list only status approved  employers details
    patch-updating details of employers
    """

    permission_classes = [IsAdminUser]

    def get(self,request,pk=None):
        employer = Employer.objects.filter(status='Approve')
        serializer = EmployerSerializer(employer,many=True)
        return Response(serializer.data)

    def patch(self,request,pk):
        user = get_object_or_404(Employer, id=pk,status='Approve')
        serializer = AdminEmployerProfileSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile reset done'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})



class EmployerPending(APIView):


    """
    this view ,get- list all  employers details except those with approved status
    patch-updating status of employers
    """
    permission_classes = [IsAdminUser]

    def get(self,request,pk=None):
        employer = Employer.objects.exclude(status='approve')
        serializer = EmployerSerializer(employer,many=True)
        return Response(serializer.data)


    def patch(self,request,pk):
        user = get_object_or_404(Employer, id=pk)
        serializer = AdminEmployerStatusSerializer(user,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Company request status changed'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})









class AllJobseeker(APIView):
    """
    this view ,get- list all  job seeker details  those with approved status
    patch-updating profile details of job seekers
    """

    permission_classes = [IsAdminUser]

    def get(self,request,pk=None):
        jobseeker = JobSeeker.objects.filter(status='Approve')
        serializer = JobseekerSerializer(jobseeker,many=True)
        return Response(serializer.data)

    def patch(self,request,pk):
        user = get_object_or_404(JobSeeker, id=pk)
        serializer = AdminJobseekerProfileSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile reset done'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})



class JobseekerPending(APIView):
    """
    this view ,get- list all  job seeker details except those with approved status
    patch-updating status of job seeker
    """

    permission_classes = [IsAdminUser]

    def get(self,request,pk=None):
        jobseeker = JobSeeker.objects.exclude(status='approve')
        serializer = JobseekerSerializer(jobseeker,many=True)
        return Response(serializer.data)


    def patch(self,request,pk):
        user = get_object_or_404(JobSeeker, id=pk)
        serializer = AdminJobSeekerStatusSerializer(user,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Job Seeker request status changed'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})



class AllJobs(APIView):
    """
    list all approved jobs with applications count
    """
    permission_classes = [IsAdminUser]

    def get(self,request):
        jobs = Jobs.objects.filter(status='Approve').annotate(total_applications=Count('applicant',distinct=True))
        serializer = AdminJobSerializer(jobs,many=True)
        return Response(serializer.data)




class JobsPending(APIView):
    """
    get-list all jobs those with status not approved
    patch-updating job status to approve /disapprove
    """
    permission_classes = [IsAdminUser]

    def get(self,request,pk=None):
        jobs = Jobs.objects.exclude(status='approve')
        serializer = AdminJobStatusSerializer(jobs,many=True)
        return Response(serializer.data)


    def patch(self,request,pk):
        job = get_object_or_404(Jobs, id=pk)
        serializer = AdminJobStatusSerializer(job,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Job status changed'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})






