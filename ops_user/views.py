from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .models import UploadedFile
from .serializer import UploadedFileSerializer

# Create your views here.
def ops_user_index(request):
    return render(request, "ops_user/index.html")

def ops_user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "ops_user/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "ops_user/signup.html", {
                "message": "Username already taken."
            })
        login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ops_user/signup.html")
    
def ops_user_signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('api-root'))
        else:
            return render(request, "ops_user/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "ops_user/login.html")
    
class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer