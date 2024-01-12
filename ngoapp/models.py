from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class statement(models.Model):
    uid = models.IntegerField()
    amount = models.CharField(max_length=100)
    screenshot = models.ImageField(upload_to ='screenshot')
    status = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)