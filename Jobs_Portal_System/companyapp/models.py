from django.db import models
from django.conf import settings



class Employer(models.Model):
    """
    model for employers table
    """
    CHOICES = [('Pending', 'Pending'),
               ('Approve', 'Approved'),
               ('Block', 'Blocked'),
               ('Remove', 'Removed')
               ]

    company=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='employer')
    company_name=models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company logo',)
    website = models.URLField(max_length=200)
    address = models.TextField()
    mobile_number = models.CharField(max_length=10,blank=True,null=True)
    status = models.CharField(max_length=10, choices=CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Jobs(models.Model):
    """
    model for job table
    """
    CHOICES = [('Pending', 'Pending'),
               ('Approve', 'Approved'),
               ('Disapprove', 'Disapproved')
               ]

    company=models.ForeignKey(Employer,on_delete=models.CASCADE,related_name='jobs')
    designation=models.CharField(max_length=200)
    description = models.TextField()
    location=models.CharField(max_length=200)
    poster = models.ImageField(upload_to='job pic')
    posting_date = models.DateTimeField(auto_now_add=True)
    last_date= models.DateField()
    requirements = models.TextField()
    status = models.CharField(max_length=10, choices=CHOICES, default='Pending')
    updated_at = models.DateTimeField(auto_now=True)

