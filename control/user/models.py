from django.db import models

# Create your models here.


class User(models.Model):
    id=models.IntegerField(primary_key=True)
    user_name=models.CharField(max_length=20)
    password=models.CharField(max_length=6)
    postionId=models.IntegerField()


class DepartmentPostion(models.Model):
    id=models.IntegerField(primary_key=True)
    department=models.CharField(max_length=20)
    position=models.CharField(max_length=20)
