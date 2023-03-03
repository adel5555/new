from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        READER = "READER",'Reader'
        AUTHOR = "AUTHOR",'Author'
    
    base_role = Role.ADMIN

    role = models.CharField(max_length=50,choices=Role.choices)
    # def save(self,*args,**kwargs):
    #     if not self.pk:
    #         self.role = self.base_role
    #         return super().save(*args,**kwargs)


class ReaderManeger(BaseUserManager):
    def get_queryset(self,*args, **kwargs):
        resultes = super().get_queryset(*args, **kwargs)
        return resultes.filter(role = User.Role.READER)
    pass

class Reader(User):
    base_role = User.Role.READER
    reader = ReaderManeger()
    class Meta:
        proxy = True
    def welcome(self):
        return "only For Reader"


@receiver(post_save, sender=Reader)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "READER":
        ReaderProfile.objects.create(user=instance)


class ReaderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reader_id = models.IntegerField(null=True,blank=True)


class AuthorManeger(BaseUserManager):
    def get_queryset(self,*args, **kwargs):
        resultes = super().get_queryset(*args, **kwargs)
        return resultes.filter(role = User.Role.AUTHOR)
    pass

class Author(User):
    base_role = User.Role.AUTHOR
    auhtor = AuthorManeger()
    class Meta:
        proxy = True
    def welcome(self):
        return "only For author"

@receiver(post_save, sender=Author)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "AUTHOR":
        AuthorProfile.objects.create(user=instance)

class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Author_id = models.IntegerField(null=True,blank=True)