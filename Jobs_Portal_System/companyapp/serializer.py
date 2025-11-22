from rest_framework import serializers
from django.core.mail import send_mail
from .models import Jobs,Employer
from jobseekerapp.models import JobSeeker,Applicant
from adminapp.serializer import EmployerSerializer
from adminapp.models import BaseProfile
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class JobSerializer(serializers.ModelSerializer):
    """
        serializer for job model
        create new job and send email notification to admin
        update job details
        """
    class Meta:
        model=Jobs
        fields=['id','designation','description','location','poster','posting_date','last_date','requirements','status','updated_at']


    def create(self, validated_data):
        request=self.context.get('request')

        if request.user.employer.status == 'Approve':
            job = Jobs.objects.create(company=request.user.employer, **validated_data)
            send_mail(
                subject='New Job Posted',
                message=f'hi, Employer posted new job   ',
                from_email=request.user.email,
                recipient_list=['jobportal@gmail.com'],
                fail_silently=False,
            )

        else:
            raise serializers.ValidationError({'message':f'your request status is {request.user.employer.status},please wait'})

        return job


    def update(self, instance, validated_data):
        instance.designation = validated_data.get('designation', instance.designation)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.last_date = validated_data.get('last_date', instance.last_date)
        instance.requirements = validated_data.get('requirements', instance.requirements)
        instance.save()

        return instance


class PasswordSerializer(serializers.ModelSerializer):
    """
        serializer for password reset
        """
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

class JobseekerSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobSeeker
        fields=['id','full_name','dob','picture','education','mobile_number']

class ApplicationJobSerializer(serializers.ModelSerializer):

    class Meta:
        model=Jobs
        fields=['id','designation','location','poster','posting_date','last_date',]


class ApplicationSerializer(serializers.ModelSerializer):
    """
        serializer for job application and updating application  status and send email with updation info
        """
    user=JobseekerSerializer(required=False)
    job = ApplicationJobSerializer(required=False)
    class Meta:
        model=Applicant
        fields=['id','user','job','status']



    def update(self, instance, validated_data):
        request=self.context.get('request')
        email=self.context.get('email')
        instance.status=validated_data.get('status',instance.status)
        instance.save()

        send_mail(
            subject='Job Status',
            message=f'hi, your job application status changed to {instance.status} ',
            from_email=request.user.email,
            recipient_list=[email],
            fail_silently=False,
        )

        return instance
