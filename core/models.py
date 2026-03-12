from django.db import models
from django.contrib.auth.models import User

class Usertype(models.Model):
    type = models.CharField(max_length=100) # 'jobseeker', 'hire'

    def __str__(self):
        return self.type

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # null=True allows users to exist without a type initially
    usertype = models.ForeignKey(Usertype, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username