from django.shortcuts import render
from django.contrib import messages
from company_signup.models import Advertisers
from user_login.models import User_Purchase_List
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.conf import settings
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
            return render(request, 'company_product.html', {'companies': t[1:],
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
        return render(request, 'company_product.html', {'companies': t[1:],
                                                        'company_name': name,
                                                        'delete_error': delete_error,
                                                        'email': email,
                                                        'password': passw,})

def delete_ad(request):
    delete_id = int(request.GET.get('id'))
    email = request.GET.get('email')
    passw = request.GET.get('password')
    user = request.GET.get('user')
    delete_id = delete_id + 1

    query = f"SELECT * FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"
    t = list(Advertisers.objects.raw(query))
    search_id = t[delete_id].id
    temp = Advertisers.objects.get(id=search_id)
    ad_name = temp.ad_name
    ad_price = temp.ad_price
    q2 = f"select * from user_login_user_purchase_list where company_email='{email}' and ad_name='{ad_name}' and ad_price='{ad_price}'"
    user_purchase_deletes = User_Purchase_List.objects.raw(q2)
    if(True):
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

def add_stop(request):
    if request.method == "POST":
        email = request.GET.get('email')
        passw = request.GET.get('password')
        user = request.GET.get('user')
        #long_lat = request.POST.get('long_lat')
        detail = request.POST.get('detail')
        stop_category = request.POST.get('stop_category')
        '''
        obj = Advertisers(company_name=user,company_email=email,company_password=passw,ad_name=detail,long_lat=long_lat,type=stop_category,ad_price=0,deleted=0)
        obj.save()
        print(f"cat = {stop_category}")

        name = user
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
        else:
            query1 = f"SELECT id,company_name FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"
            name = tuple(Advertisers.objects.raw(query1))[0]
            # return render(request, 'company_product.html', {'companies': Advertisers.objects.get(company_email=email)})
            return render(request, 'company_product.html', {'companies': t[1:],
                                                            'company_name': name,
                                                            'email': email,
                                                            'password': passw, })'''
        settings.email1 = email
        settings.passw1 = passw
        settings.user1 = user
        settings.detail1 = detail
        settings.stop_category1 = stop_category
        return render(request, 'add_stop_location.html', {  'company_name': user,
                                                            'email': email,
                                                            'password': passw,
                                                            'detail' : detail,
                                                            'stop_category': stop_category })

    else:
        email = request.GET.get('email')
        passw = request.GET.get('password')
        user = request.GET.get('user')
        return render(request, 'add_stop.html',     {   'company_name': user,
                                                        'email': email,
                                                        'password': passw, })

#def add_stop_loc(request,lat1,long1,email,passw,user,detail,stop_category):
def add_stop_loc(request, lat1, long1):

    '''email = request.GET.get('email')
    passw = request.GET.get('password')
    user = request.GET.get('user')
    detail = request.GET.get('detail')
    stop_category = request.GET.get('stop_category')
    #lat1 = request.GET.get('lat1')
    #long1 = request.GET.get('long1')'''
    email = settings.email1
    passw = settings.passw1
    user = settings.user1
    detail = settings.detail1
    stop_category = settings.stop_category1
    print(lat1)
    print(long1)
    latlng = request.GET.get('latlng')
    print(latlng)

    obj = Advertisers(company_name=user, company_email=email, company_password=passw, ad_name=detail, latitude=lat1,
                      type=stop_category, ad_price=0, deleted=0, longitude=long1)
    obj.save()
    name = user
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
    else:
        query1 = f"SELECT id,company_name FROM company_signup_advertisers WHERE company_email = '{email}' AND company_password = '{passw}'"
        name = tuple(Advertisers.objects.raw(query1))[0]
        # return render(request, 'company_product.html', {'companies': Advertisers.objects.get(company_email=email)})
        return render(request, 'company_product.html', {'companies': t[1:],
                                                        'company_name': name,
                                                        'email': email,
                                                        'password': passw, })