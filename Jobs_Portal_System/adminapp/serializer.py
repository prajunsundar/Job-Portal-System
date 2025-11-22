from .models import BaseProfile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random
from django.core.mail import send_mail
from companyapp.models import Jobs,Employer
from jobseekerapp.models import JobSeeker,Applicant
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    serializer for base profile model
    """
    class Meta:
        model=BaseProfile
        fields=['id','email','role','password']


class ListBaseProfileSerializer(serializers.ModelSerializer):
    """
    serializer for base profile model
    """
    class Meta:
        model=BaseProfile
        fields=['id','email']


class JobseekerSerializer(serializers.ModelSerializer):
    """
        serializer for job seeker model
        """
    users = ListBaseProfileSerializer(required=False)
    class Meta:
        model=JobSeeker
        fields=['users','id','full_name','dob','picture','education','address','mobile_number','status']


class EmployerSerializer(serializers.ModelSerializer):
    """
        serializer for employer model
        """
    company=ListBaseProfileSerializer(required=False)
    class Meta:
        model=Employer
        fields=['company','id','company_name','logo','website','address','mobile_number','status']








def generatePassword():
    """
    generate 6 digit number for temp password
    """
    temp_password=random.randint(100000,999999)
    return temp_password



class AdminRegisterSerializer(serializers.ModelSerializer):
    """
        serializer for admin registration
        validate-check email already exist or not
        create-create new user and send plain text notification email to user
        """
    role=serializers.CharField(max_length=10,default='Admin')
    class Meta:
        model=BaseProfile
        fields=['email','role']

    def validate(self,data):
        if BaseProfile.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'message':'email already exists'})

        return data
    def create(self, validated_data):
        otp=generatePassword()

        user=BaseProfile.objects.create_user(email=validated_data['email'],role=validated_data['role'],password=str(otp),is_staff=True)
        send_mail(
            subject='login password',
            message=f'hi  your temporary log in password is {otp}',
            from_email='jobportal@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user




class EmployerRegisterSerializer(serializers.ModelSerializer):
    """
            serializer for employer registration
            validate-check email already exist or not
            create-create new user and send plain text notification email to employer and admin
            """
    employer=EmployerSerializer(required=False)
    role=serializers.CharField(max_length=10,default='Employer')

    class Meta:
        model=BaseProfile
        fields=['email','role','employer']


    def validate(self,data):
        if BaseProfile.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'message':'email already exists'})

        return data

    def create(self, validated_data):
        employer_data=validated_data.pop('employer',[])

        otp=generatePassword()

        user=BaseProfile.objects.create_user(email=validated_data['email'],role=validated_data['role'],password=str(otp))
        send_mail(
            subject='login password',
            message=f'hi  your temporary log in password is {otp}',
            from_email='jobportal@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        Employer.objects.create(company_id=user.id,**employer_data)

        send_mail(
            subject='New Employer Register',
            message=f'hi, new employer registred ',
            from_email=user.email,
            recipient_list=['jobportal@gmail.com'],
            fail_silently=False,
        )



        return user






class JobseekerRegisterSerializer(serializers.ModelSerializer):
    """
                serializer for job seeker registration
                validate-check email already exist or not
                create-create new user and send plain text notification email to job seeker and admin
                """

    jobseeker=JobseekerSerializer(required=False)
    role=serializers.CharField(max_length=10,default='Job Seeker')

    class Meta:
        model=BaseProfile
        fields=['email','role','jobseeker']

    def validate(self,data):
        if BaseProfile.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'message':'email already exists'})

        return data

    def create(self, validated_data):

        jobseeker_data=validated_data.pop('jobseeker',[])

        otp=generatePassword()

        user=BaseProfile.objects.create_user(email=validated_data['email'],role=validated_data['role'],password=str(otp))
        JobSeeker.objects.create(users=user,**jobseeker_data)

        send_mail(
            subject='New Job Seeker Register',
            message=f'hi, new job seeker registred ',
            from_email=user.email,
            recipient_list=['jobportal@gmail.com'],
            fail_silently=False,
        )

        send_mail(
            subject='login password',
            message=f'hi  your temporary log in password is {otp}',
            from_email='jobportal@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )


        return user




class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token=super().get_token(user)
        token['email']=user.email
        token['role']=user.role
        return token



class AdminPasswordSerializer(serializers.ModelSerializer):
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
        else:
            raise serializers.ValidationError({'message': 'passwords didnt match'})

        return instance





class AdminEmployerProfileSerializer(serializers.ModelSerializer):
    """
        serializer for employer profile reset
        """
    class Meta:
        model = Employer
        fields = ['company_name', 'logo', 'website', 'address', 'mobile_number']



    def update(self, instance, validated_data):
        instance.company_name=validated_data.get('company_name',instance.company_name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.website = validated_data.get('website', instance.website)
        instance.address = validated_data.get('address', instance.address)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.save()

        return instance


class AdminEmployerStatusSerializer(serializers.ModelSerializer):
    """
        serializer for employer status updating
        """
    class Meta:
        model = Employer
        fields = ['status']


    def update(self, instance, validated_data):
        instance.status=validated_data.get('status',instance.status)
        instance.save()
        return instance








class AdminJobseekerProfileSerializer(serializers.ModelSerializer):
    """
        serializer for job seeker profile updating
        """
    class Meta:
        model = JobSeeker
        fields = ['full_name', 'dob', 'picture', 'education', 'address', 'mobile_number']



    def update(self, instance, validated_data):
        instance.full_name=validated_data.get('full_name',instance.full_name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.education=validated_data.get('education',instance.education)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance


class AdminJobSeekerStatusSerializer(serializers.ModelSerializer):
    """
        serializer for updating job seeker request status
        """
    class Meta:
        model = JobSeeker
        fields = ['status']


    def update(self, instance, validated_data):
        instance.status=validated_data.get('status',instance.status)
        instance.save()
        return instance




class AdminJobSerializer(serializers.ModelSerializer):
    """
        serializer for showing jobs with application count
        """
    total_applications=serializers.IntegerField()
    class Meta:
        model=Jobs
        fields=['id','company','designation','description','location','poster','posting_date','last_date',
                'requirements','status','total_applications','updated_at']




class AdminJobStatusSerializer(serializers.ModelSerializer):
    """
    serializer for updating job status
    """
    class Meta:
        model = Jobs
        fields = ['id','company','designation','posting_date','last_date','status']


    def update(self, instance, validated_data):
        instance.status=validated_data.get('status',instance.status)
        instance.save()
        return instance

