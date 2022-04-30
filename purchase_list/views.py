from django.shortcuts import render
from user_signup.models import Users
from user_login.models import User_Purchase_List
from company_signup.models import Advertisers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
# Create your views here.
def user_purchase_list(request):
    user_email = request.GET.get('email')
    user_pass = request.GET.get('password')

    if request.method == "POST":
        q = f"select * from user_login_user_purchase_list where user_email = '{user_email}' and active = '1'"
        purchased = User_Purchase_List.objects.raw(q)
        n = len(purchased)
        for i in range(0,n):
            new_rating = request.POST.get(f"test{i}")
            print(new_rating)
            p = purchased[i]
            search_id = p.id
            temp = User_Purchase_List.objects.get(id = search_id)
            if new_rating != 'NULL':
                temp.rating = new_rating
                temp.save()
    try:
        query2 = f"select id, user_name from user_login_user_purchase_list where user_email = '{user_email}' and active = '1'"
        user_name = tuple(Users.objects.raw(query2))[0]
    except:
        query2 = f"SELECT id, user_name FROM user_signup_users WHERE user_email = '{user_email}' AND user_password = '{user_pass}'"
        user_name = tuple(Users.objects.raw(query2))[0]

    query3 = f"select * from user_login_user_purchase_list where user_email = '{user_email}' and active = '1'"
    user_purchases = tuple(Users.objects.raw(query3))

    return render(request, 'user_purchase.html', {'user': Users.objects.get(user_email=user_email),
                                                  'user_name': user_name,
                                                  'user_email': user_email,
                                                  'user_pass': user_pass,
                                                  'user_purchases':user_purchases})
    #return HttpResponse(f"{user_email}, {user_pass}")

def user_purchase_delete(request):
    delete_id = int(request.GET.get('id'))
    user_email = request.GET.get('email')
    user_pass = request.GET.get('password')
    q = f"select * from user_login_user_purchase_list where user_email = '{user_email}' and active = '1'"
    purchased = User_Purchase_List.objects.raw(q)
    n = len(purchased)

    p = purchased[delete_id]
    search_id = p.id
    temp = User_Purchase_List.objects.get(id=search_id)
    company_email = temp.company_email
    ad_name = temp.ad_name
    ad_price = temp.ad_price
    temp.active = 0
    temp.save()

    q1 = f"select * from company_signup_advertisers where company_email='{company_email}' and ad_name='{ad_name}' and ad_price='{ad_price}' and deleted='1'"
    delete_ad = Advertisers.objects.raw(q1)
    q2 = f"select * from user_login_user_purchase_list where company_email='{company_email}' and ad_name='{ad_name}' and ad_price='{ad_price}'"
    user_purchase_deletes = User_Purchase_List.objects.raw(q2)
    if(len(list(delete_ad))>0):
        delete_ad_id = delete_ad[0].id
        temp = Advertisers.objects.get(id=delete_ad_id)
        temp.delete()
        for t in user_purchase_deletes:
            delete_purchase_id = t.id
            temp= User_Purchase_List.objects.get(id=delete_purchase_id)
            temp.delete()

    try:
        query2 = f"select id, user_name from user_login_user_purchase_list where user_email = '{user_email}'"
        user_name = tuple(Users.objects.raw(query2))[0]
    except:
        query2 = f"SELECT id, user_name FROM user_signup_users WHERE user_email = '{user_email}' AND user_password = '{user_pass}'"
        user_name = tuple(Users.objects.raw(query2))[0]

    query3 = f"select * from user_login_user_purchase_list where user_email = '{user_email}' and active = '1'"
    user_purchases = tuple(Users.objects.raw(query3))

    '''return render(request, 'user_purchase.html', {'user': Users.objects.get(user_email=user_email),
                                                  'user_name': user_name,
                                                  'user_email': user_email,
                                                  'user_pass': user_pass,
                                                  'user_purchases':user_purchases})'''
    #return HttpResponse(f"{user_email}, {user_pass}")
    base_url = "http://127.0.0.1:8000/user_login/user_purchase_list/"
    query_string = urlencode({'email': user_email, 'password': user_pass})
    url = '{}?{}'.format(base_url, query_string)
    return HttpResponseRedirect(url)
