from django.shortcuts import render
from .models import Users
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def signup_user(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('email')
        user_phone = request.POST.get('phone')
        user_pass = request.POST.get('password')

        if (len(user_phone) != 10) or (not user_phone.isdigit()):
            messages.success(request, "Incorrect details for existing company user")
            return HttpResponseRedirect("http://127.0.0.1:8000/")
        try:
            obj = Users(user_name=user_name, user_email=user_email, user_phone=user_phone, user_password=user_pass)
            obj.save()
        except:
            messages.success(request, "Incorrect details for existing company user")
            return HttpResponseRedirect("http://127.0.0.1:8000/")
    return render(request, "user_signup.html")