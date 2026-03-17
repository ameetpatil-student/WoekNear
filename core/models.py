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
class StoreProfile(models.Model):
    # Links this profile to the login account
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # 1. Name
    name = models.CharField(max_length=100)
    
    # 2. Email
    email = models.EmailField()
    
    # 3. Store Name
    store_name = models.CharField(max_length=150)
    
    # --- NEW FIELDS ADDED HERE ---
    category = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # -----------------------------
    
    # 4. Store Location 
    store_location = models.CharField(max_length=255)
    
    # 5. Mobile Number
    mobile_number = models.CharField(max_length=15)
    
    # Document Upload (Allows PDFs, JPGs, PNGs, etc.)
    verification_document = models.FileField(
        upload_to='verifications/documents/', 
        help_text="Please upload your GST certificate or a recent electricity bill."
    )
    
    # Internal status for you as the admin
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.store_name} ({self.name})"