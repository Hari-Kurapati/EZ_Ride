from django.shortcuts import render
from django.contrib import messages
from company_signup.models import Advertisers
from user_login.models import User_Purchase_List
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
# Create your views here.
def company_signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        query = f"SELECT * FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"

        t = list(Advertisers.objects.raw(query))

        rating_list = []
        i = 0
        for item in t:
            rating_query = f"select id,avg(rating) as avg from user_login_user_purchase_list " \
                           f"where company_email = '{item.company_email}' and ad_name='{item.ad_name}' and ad_price='{item.ad_price}' and rating IS NOT NULL"
            avg_rating = tuple(User_Purchase_List.objects.raw(rating_query))
            if not (avg_rating[0].avg):
                avg_rating = -1
            else:
                avg_rating = avg_rating[0].avg
            rating_list.append(avg_rating)
            t[i].rating = "{:.1f}".format(avg_rating)
            i = i + 1

        i = 0
        for item in t:
            company_email = item.company_email
            ad_name = item.ad_name
            ad_price = item.ad_price
            q1 = f"select * from user_login_user_purchase_list where company_email='{company_email}' and ad_name='{ad_name}' and ad_price='{ad_price}' and active='1'"
            user_details = list(User_Purchase_List.objects.raw(q1))
            if(len(user_details)>0):
                user_details = user_details[0]
                t[i].user_name = user_details.user_name
                t[i].user_email = user_details.user_email
            else:
                t[i].user_name = "N/A"
                t[i].user_email = "N/A"
            i = i + 1

        if t==[]:
            messages.success(request, "Incorrect email address or password")
        else:
            query1 = f"SELECT id,company_name FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"
            name = tuple(Advertisers.objects.raw(query1))[0]
            #return render(request, 'company_product.html', {'companies': Advertisers.objects.get(company_email=email)})
            return render(request, 'company_product.html', {'companies': t,
                                                            'company_name': name,
                                                            'email': email,
                                                            'password': passw,})

    return render(request, 'company_signin.html')

def company_ads_list(request):
    email = request.GET.get('email')
    passw = request.GET.get('password')
    delete_error = request.GET.get('delete_error')

    query = f"SELECT * FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"

    t = list(Advertisers.objects.raw(query))

    rating_list = []
    i = 0
    for item in t:
        rating_query = f"select id,avg(rating) as avg from user_login_user_purchase_list " \
                       f"where company_email = '{item.company_email}' and ad_name='{item.ad_name}' and ad_price='{item.ad_price}' and rating IS NOT NULL"
        avg_rating = tuple(User_Purchase_List.objects.raw(rating_query))
        if not (avg_rating[0].avg):
            avg_rating = -1
        else:
            avg_rating = avg_rating[0].avg
        rating_list.append(avg_rating)
        t[i].rating = "{:.1f}".format(avg_rating)
        i = i + 1

    i = 0
    for item in t:
        company_email = item.company_email
        ad_name = item.ad_name
        ad_price = item.ad_price
        q1 = f"select * from user_login_user_purchase_list where company_email='{company_email}' and ad_name='{ad_name}' and ad_price='{ad_price}' and active='1'"
        user_details = list(User_Purchase_List.objects.raw(q1))
        if (len(user_details) > 0):
            user_details = user_details[0]
            t[i].user_name = user_details.user_name
            t[i].user_email = user_details.user_email
        else:
            t[i].user_name = "N/A"
            t[i].user_email = "N/A"
        i = i + 1

    if t == []:
        messages.success(request, "Incorrect email address or password")
        return HttpResponseRedirect("http://127.0.0.1:8000/")
    else:
        query1 = f"SELECT id,company_name FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"
        name = tuple(Advertisers.objects.raw(query1))[0]
        # return render(request, 'company_product.html', {'companies': Advertisers.objects.get(company_email=email)})
        return render(request, 'company_product.html', {'companies': t,
                                                        'company_name': name,
                                                        'delete_error': delete_error,
                                                        'email': email,
                                                        'password': passw,})

def delete_ad(request):
    delete_id = int(request.GET.get('id'))
    email = request.GET.get('email')
    passw = request.GET.get('password')
    user = request.GET.get('user')

    query = f"SELECT * FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"
    t = list(Advertisers.objects.raw(query))
    search_id = t[delete_id].id
    temp = Advertisers.objects.get(id=search_id)
    ad_name = temp.ad_name
    ad_price = temp.ad_price
    q2 = f"select * from user_login_user_purchase_list where company_email='{email}' and ad_name='{ad_name}' and ad_price='{ad_price}'"
    user_purchase_deletes = User_Purchase_List.objects.raw(q2)
    if(user=="N/A"):
        temp.delete()
        delete_error = 0
        for purchase in user_purchase_deletes:
            delete_purchase_id = purchase.id
            temp= User_Purchase_List.objects.get(id=delete_purchase_id)
            temp.delete()
    else:
        temp.deleted = 1
        temp.save()
        delete_error = 1

    base_url = "http://127.0.0.1:8000/company_login/company_ads_list"
    query_string = urlencode({'email': email, 'password': passw, 'delete_error':delete_error})
    url = '{}?{}'.format(base_url, query_string)
    return HttpResponseRedirect(url)