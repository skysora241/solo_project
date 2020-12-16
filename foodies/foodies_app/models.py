from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters!"
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name should be at least 2 characters!"
        if not email_check.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['email']) <5:
            errors['email'] = ("Invalid email address!")
        if len(postData['pw']) <8:
            errors['pw'] = "Password should be at least 8 characters!"
        if postData['pw'] != postData['conf_pw']:
            errors['conf_pw'] = "Password and confirm password must match!"
        return errors
class Market(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    desc_m = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    market = models.ForeignKey(Market, related_name="items", on_delete=models.CASCADE)
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(Item, related_name="users")

    objects =UserManager()