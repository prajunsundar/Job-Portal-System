from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from .models import JobSeeker,Applicant
from .serializer import ApplicantSerializer,PasswordSerializer,AccountSerializer,JobSerializer
from rest_framework import status
from adminapp.models import BaseProfile
from rest_framework.views import APIView
from .permission import IsJobSeeker
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from companyapp.models import Employer,Jobs




class PasswordReset(APIView):
    """
    for reseting users password
    """
    permission_classes = [IsJobSeeker]

    def put(self,request):
        user=get_object_or_404(BaseProfile,id=request.user.id)
        serializer=PasswordSerializer(user,data=request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Job seeker password reset done'},status=status.HTTP_205_RESET_CONTENT)
        return Response({'message':serializer.errors})



class MyAccount(APIView):
    """
    get-show logged in user profile data
    patch-update picture,education details and address
    """
    permission_classes = [IsJobSeeker]
    def get(self,request):
        user=JobSeeker.objects.get(users_id=request.user.id)
        serializer=AccountSerializer(user)
        return Response(serializer.data)


    def patch(self,request):
        user = get_object_or_404(JobSeeker, users_id=request.user.id)
        serializer = AccountSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile details updated'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': serializer.errors})




class MyApplications(APIView):
    """
    get-list all applications submited by user
    post-apply for new job
    """
    permission_classes = [IsJobSeeker]
    def get(self,request):
        mine=Applicant.objects.filter(user__users_id=request.user.id)
        serializer=ApplicantSerializer(mine,many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer=ApplicantSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Job application applied'},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors})



class JobList(generics.ListAPIView):
    """
    list all jobs by filter and searching keywords like designation,location
    """
    permission_classes = [IsJobSeeker]
    queryset = Jobs.objects.filter(status='Approve')
    serializer_class = JobSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['location', 'designation']

    search_fields = ['designation', 'location']
