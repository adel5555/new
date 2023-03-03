from django.contrib.auth.forms import UserCreationForm

from django.db import transaction
from django import forms
from .models import User,ReaderProfile,AuthorProfile
choise = (("READER","Reader"),("AUTHOR","Author"))
class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=choise)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username","email","role"]
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role')
        # if("READER" in self.cleaned_data.get('role')):
        #     user.role = ("READER",'Reader')
        # else:
        #     user.role = ("AUTHOR",'Author')
        user.save()
        if(user.role == "READER"):
            reader = ReaderProfile.objects.create(user=user)
            reader.save()
            
        elif(user.role == "AUTHOR"):
            author = AuthorProfile.objects.create(user=user)
            author.save()
        return user
