from django.db import models
from django.contrib.auth.models import User


class Usertype(models.Model):
    type = models.CharField(max_length=100) 

    def __str__(self):
        return self.type

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.ForeignKey(Usertype, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
# NOTICE: StoreProfile is now fully separated from Profile

class StoreProfile(models.Model):
    employer = models.OneToOneField(User, on_delete=models.CASCADE) # Links profile to the logged-in user
    
    # Store Details from your HTML form
    owner_name = models.CharField(max_length=100)
    email = models.EmailField()
    store_name = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField()
    mobile_number = models.CharField(max_length=15)
    
    # Document upload (Requires configuring MEDIA_URL in settings.py)
    verification_document = models.FileField(upload_to='verification_docs/')
    
    # THE APPROVAL LOCK
    is_approved = models.BooleanField(default=False) # Defaults to False when they first submit
    admin_remarks = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store_name} - {'Approved' if self.is_approved else 'Pending'}"
    
class adminlogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    


class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    job_timing = models.CharField(max_length=100, blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

class Ad(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255) # Maps to job_title in your Ad form
    location = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Prevent duplicate applications
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} → {self.job.job_title}"