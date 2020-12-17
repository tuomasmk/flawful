from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500)