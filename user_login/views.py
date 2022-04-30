from django.shortcuts import render
from django.contrib import messages
from user_signup.models import Users
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
import sys

# Create your views here.
def user_login(request):
    if request.method == "POST":
        user_email = request.POST.get('email')
        user_pass = request.POST.get('password')

        query = f"SELECT * FROM user_signup_users WHERE user_email = '{user_email}' AND user_password = '{user_pass}'"

        t = tuple(Users.objects.raw(query))

        try:
            query2 = f"SELECT id, user_name FROM user_signup_users WHERE user_email = '{user_email}' AND user_password = '{user_pass}'"
            user_name = tuple(Users.objects.raw(query2))[0]
        except:
            user_name = "Nope"

        query3 = f"select * from user_login_user_purchase_list where user_email = '{user_email}'"
        user_purchases = tuple(Users.objects.raw(query3))

        if t==():
            
            messages.success(request, "Incorrect email address or password")
        else:
            #return render(request, 'user_purchase.html', {'user': Users.objects.get(user_email=user_email),
            #                                              'user_name': user_name,
            #                                              'user_purchases':user_purchases})
            #return HttpResponseRedirect('user_purchase_list/')
            base_url = "http://127.0.0.1:8000/user_login/user_purchase_list/"
            query_string = urlencode({'email' : user_email, 'password': user_pass})
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)

    return render(request, "user_signin.html")


