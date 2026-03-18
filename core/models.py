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
from django.db import models
from django.contrib.auth.models import User # Assuming employers log in with standard Django auth

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
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store_name} - {'Approved' if self.is_approved else 'Pending'}"
    
class adminlogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username