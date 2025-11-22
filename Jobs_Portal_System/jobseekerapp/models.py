from django.db import models
from django.conf import settings
from companyapp.models import Jobs,Employer



class JobSeeker(models.Model):
    """
    model for job seeker table
    """
    CHOICES = [('Pending', 'Pending'),
               ('Approve','Approved'),
               ('Block','Blocked'),
               ('Remove','Removed')
               ]

    users=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='jobseeker')
    full_name=models.CharField(max_length=200)
    dob=models.DateField(null=True,blank=True)
    picture=models.ImageField(upload_to='job seeker pics',blank=True,null=True)
    education=models.TextField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    mobile_number = models.CharField(max_length=10,blank=True,null=True)
    status=models.CharField(max_length=10,choices=CHOICES,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class Applicant(models.Model):
    """
    model for application table
    """
    APPLICATION_CHOICES=[('Pending','Pending'),
                         ('Accepted','Accepted'),
                         ('Rejected','Rejected'),
                         ('Viewed','Viewed'),
                         ('Visited','Visited')
                         ]
    user=models.ForeignKey(JobSeeker,on_delete=models.CASCADE,related_name='applicant')
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE,related_name='applicant')
    status=models.CharField(max_length=200,choices=APPLICATION_CHOICES,default='Pending')
    applied_date = models.DateTimeField(auto_now_add=True)


