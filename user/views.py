from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.views.generic import CreateView
from django.contrib.auth import login,authenticate
from django.urls import reverse_lazy
from .form import SignupForm
from .models import User

# Create your views here.
def home(request):
    return HttpResponse("new")


class register(CreateView):
    model = User
    form_class = SignupForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

