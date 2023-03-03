from django.db import models
from django.core.validators import MinLengthValidator,FileExtensionValidator
from time import timezone
from django.conf import settings
# Create your models here.

class Book(models.Model):
    name = models.CharField( max_length=50,validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    MaxPageNumber = models.IntegerField(null=True)
    text_book = models.FileField(upload_to="AllBooks",validators=[FileExtensionValidator('txt','only text file please')],null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.name

class Pages(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.IntegerField()
    content = models.CharField(max_length=600)



class Reading(models.Model):
    Reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    continue_reading_from_this_page = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.Reader
    

