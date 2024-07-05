from typing import Any, Iterable
from django.db import models

from bot.mail import mail_user

# Create your models here.
def user_directory_path(x,y):
    return

class CustomUser(models.Model):
    username = models.TextField()
    full_name = models.TextField()
    email = models.EmailField( max_length=254,blank=True,null=True)
    confirmed_email = models.BooleanField(default=False)


    def __str__(self):
        return self.username
    
    def confirm_user_email(self):
        self.confirmed_email = True
        self.save()


class UploadedApp(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField( max_length=254)
    company_name =  models.CharField(max_length=200)
    app_name = models.CharField(max_length=200)
    platform = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    estimated_size = models.CharField(max_length=200)
    #images for app
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/',blank=True,null=True)
    image3 = models.ImageField(upload_to='images/',blank=True,null=True)

    app = models.FileField(upload_to='apps/')


    def save(self, *args, **kwargs) -> None:
        # todo SEND EMAIL TO ADMIN THAT A USER UPLOADED APP
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        self.image1.delete()
        self.image2.delete()
        self.image3.delete()
        self.app.delete()
        return super().delete(*args, **kwargs)