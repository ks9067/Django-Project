from django.db import models

# Create your models here.
class Contact(models.Model):
    email=models.CharField(max_length=50)
    desc=models.TextField()
    date=models.DateField()

    def __str__(self):
        return self.email
    
class Totpkey(models.Model):
    key=models.CharField(max_length=200)
    username=models.CharField(max_length=200)

    def __str__(self):
        return self.username
