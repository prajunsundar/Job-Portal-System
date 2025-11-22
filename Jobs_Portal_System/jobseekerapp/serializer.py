from rest_framework import serializers
from .models import JobSeeker,Applicant
from companyapp.models import Employer,Jobs
from adminapp.serializer import JobseekerSerializer
from adminapp.models import BaseProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class AccountSerializer(serializers.ModelSerializer):
    """
        serializer for showing and managing user profile data
        """
    class Meta:
        model=JobSeeker
        fields=['full_name','dob','picture','education','address','mobile_number','status']


    def update(self, instance, validated_data):
        instance.picture=validated_data.get('picture',instance.picture)
        instance.education = validated_data.get('education', instance.education)
        instance.address = validated_data.get('address', instance.address)
        instance.mobile_number=validated_data.get('mobile_number',instance.mobile_number)
        instance.save()

        return instance




class PasswordSerializer(serializers.ModelSerializer):

    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model=BaseProfile
        fields=['password','confirm_password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def update(self, instance, validated_data):
        password=validated_data.get('password')
        confirm_password=validated_data.get('confirm_password')

        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError({'message':error.messages})

        if password == confirm_password:
            instance.set_password(password)
            instance.save()

        return instance





class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model=Jobs
        fields=['id','designation','description','location','poster','posting_date','last_date']

class ApplicantSerializer(serializers.ModelSerializer):
    """
        serializer for applying applications
        """
    job=serializers.PrimaryKeyRelatedField(queryset=Jobs.objects.all())
    class Meta:
        model=Applicant
        fields=['job','applied_date','status']



    def create(self, validated_data):
        request=self.context.get('request')
        if request.user.jobseeker.status == "Approve":
            application=Applicant.objects.create(user=request.user.jobseeker,**validated_data)
        else:
            raise serializers.ValidationError({'message':f'your request status is {request.user.jobseeker.status},please wait'})

        return application




