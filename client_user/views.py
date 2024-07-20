import os
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from flask_mail import force_text
from django.utils.http import urlsafe_base64_decode

from FileSharing import settings
from ops_user.models import UploadedFile

User = get_user_model()

def client_user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "client_user/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.is_active = False # Deactivate account until it is confirmed
            user.save()

            # Send email confirmation
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/email_confirmation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return HttpResponseRedirect(reverse('account_email'))
        except IntegrityError:
            return render(request, "client_user/signup.html", {
                "message": "Username already taken."
            })
    else:
        return render(request, "client_user/signup.html")
    
def client_user_signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("file_list"))
        else:
            return render(request, "client_user/signin.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "client_user/signin.html")

def download_file_view(request, file_id):
    if request.user.is_authenticated:
        file_record = get_object_or_404(UploadedFile, id=file_id)
        file_url = os.path.join(settings.MEDIA_URL, file_record.file.name)
        
        response_data = {
            "download-link": request.build_absolute_uri(file_url),
            "message": "success"
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({"message": "Unauthorized"}, status=401)
    
def file_list_view(request):
    if request.user.is_authenticated:
        files = UploadedFile.objects.all()
        return render(request, "client_user/downloads.html", {"files": files})
    else:
        return render(request, "client_user/signin.html", {"message": "Please log in to view files."})
    
def confirm_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Activation link is invalid!')
    
def email_sent(request):
    return render(request, 'account/email_sent.html')