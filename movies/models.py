from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.

class Collection(models.Model):
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=100,blank=False)
    description=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='collections')

class Movie(models.Model):
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=100,blank=False)
    description=models.TextField()
    genres=models.CharField(max_length=100)
    collection=models.ManyToManyField(Collection,related_name='movies')

class RequestCount(models.Model):
    count=models.PositiveIntegerField(default=0)