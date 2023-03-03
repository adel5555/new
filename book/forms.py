from django import forms
from .models import Book,Pages
class Bookform(forms.ModelForm):
    class Meta:
        model =Book
        fields = ['name','text_book']

    # def save(self, commit: bool = ...):

    #     return super().save(commit)
    # pass
    