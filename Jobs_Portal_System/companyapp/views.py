from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from .models import Employer,Jobs
from .serializer import JobSerializer,PasswordSerializer,ApplicationSerializer
from adminapp.serializer import EmployerSerializer
from .permission import IsEmployer
from rest_framework.views import APIView
from rest_framework import status
from jobseekerapp.models import JobSeeker,Applicant
from adminapp.models import BaseProfile

class AllJobs(APIView):
    """
    get-list all jobs posted by the loggedin employer
    post-add new job post only if admin approve the registration request
    patch-updating job details
    delete-deleting jobs of logged in employer
    """
    permission_classes = [IsEmployer]

    def get(self,request,pk=None):
        job = Jobs.objects.filter(company__company=request.user)
        serializer = JobSerializer(job,many=True)
        return Response(serializer.data)



    def post(self,request):
        serializer=JobSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'New Job Posted Successfully'},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors})



    def patch(self,request,pk):
        job = get_object_or_404(Jobs, id=pk,company__company=request.user)
        serializer = JobSerializer(job,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Job details updated'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})


    def delete(self,request,pk):
        job = get_object_or_404(Jobs, id=pk,company__company=request.user)
        job.delete()
        return Response({'message': 'job post deleted successfully'}, status=status.HTTP_200_OK)





class PasswordReset(APIView):
    """
    this view handles employer password reseting with validation
    """
    permission_classes = [IsEmployer]

    def put(self,request):
        user=get_object_or_404(BaseProfile,id=request.user.id)
        serializer=PasswordSerializer(user,data=request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Employer password reset done'},status=status.HTTP_205_RESET_CONTENT)
        return Response({'message':serializer.errors})




class AllJobsApplication(APIView):
    """
    get-list all the applications for jobs posted by logged in employer
    patch-update users application status to accepted,viewd,rejected etc
    """

    permission_classes = [IsEmployer]

    def get(self,request,pk=None):
        job = Jobs.objects.filter(company__company=request.user)
        application=Applicant.objects.filter(job__in=job)
        serializer = ApplicationSerializer(application,many=True)
        return Response(serializer.data)

    def patch(self,request,pk):
        application = get_object_or_404(Applicant, id=pk)
        email = application.user.users.email
        serializer = ApplicationSerializer(application,data=request.data,partial=True,context={'request':request,'email':email})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Application status updated'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})




