from django.shortcuts import render
from django.contrib import messages
from .models import Advertisers, Ads_catagory
from django.http import HttpResponseRedirect

# Create your views here.
def signup_comp(request):
    display_catagory = Ads_catagory.objects.all()
    if request.method=="POST":
        print(request.POST.get('ad_catagory'))
        company_name = request.POST.get('company_name')
        company_phone = request.POST.get('phone')
        company_email = request.POST.get('email')
        company_password = request.POST.get('password')
        ad_name = request.POST.get('ad_catagory')
        ad_name = "None"
        ad_price = request.POST.get('ad_price')
        ad_price = 0

        query = f"SELECT * FROM company_signup_advertisers WHERE company_email = '{company_email}'"

        t = list(Advertisers.objects.raw(query))

        if(len(company_phone)!=10) or (not company_phone.isdigit()):
            messages.success(request, "Incorrect details for existing company user")
            return HttpResponseRedirect("http://127.0.0.1:8000/")

        if(len(t)!=0):
            t = t[0]
            if((t.company_name!=company_name) or (t.company_phone!=company_phone) or (t.company_password!=company_password)):
                messages.success(request, "Incorrect details for existing company user")
                return HttpResponseRedirect("http://127.0.0.1:8000/")

        obj = Advertisers(company_name=company_name, company_phone=company_phone, company_email=company_email, company_password=company_password, ad_name=ad_name, ad_price=ad_price, deleted=0)
        obj.save()
        messages.success(request, 'You are successfully registerted')
    return render(request, "company_signup.html", {"Ads_catagory": display_catagory})
