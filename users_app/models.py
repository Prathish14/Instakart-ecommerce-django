from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    desc=models.TextField(max_length=500)

    def __str__(self):
        return self.subject


class Newsletter(models.Model):
    email=models.EmailField()

    def __str__(self):
        return self.email
    


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=True,null=True)
    image=models.ImageField(null=True,blank=True,upload_to='profile/')
    email=models.EmailField(max_length=100,blank=True,null=True)
    phone=models.CharField(max_length=60,blank=True,null=True)
    address=models.TextField(max_length=200,blank=True,null=True)
    website=models.CharField(max_length=100,blank=True,null=True)
    facebook=models.CharField(max_length=100,blank=True,null=True)
    twitter=models.CharField(max_length=100,blank=True,null=True)
    linkedin=models.CharField(max_length=100,blank=True,null=True)

    
        

    def __str__(self):
        return self.email




    



