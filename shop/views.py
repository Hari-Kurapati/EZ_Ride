from django.shortcuts import render
from django.http import HttpResponse
from user_signup.models import Users
from user_login.models import User_Purchase_List
from company_signup.models import Advertisers
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
# Create your views here.

def shop(request):
    user_email = request.GET.get('email')
    user_pass = request.GET.get('password')
    q = f"select company_signup_advertisers.id, company_signup_advertisers.company_name, company_signup_advertisers.company_phone, company_signup_advertisers.company_email, company_signup_advertisers.ad_price, company_signup_advertisers.ad_name" \
        f" from company_signup_advertisers left join (select company_name, company_phone, company_email, ad_name, ad_price, sum(active) as active from user_login_user_purchase_list group by company_name, company_phone, company_email, ad_name, ad_price) as T " \
        f"on ((company_signup_advertisers.company_name=T.company_name) and (company_signup_advertisers.ad_name=T.ad_name) and (company_signup_advertisers.ad_price=T.ad_price))" \
        f"where T.ad_name IS NULL or (T.active = '0' or T.active IS NULL)"
    if request.method == "POST":
        sort_by = request.POST.get("sort_by")
        sort_order = request.POST.get("sort_order")
        order_query = f" order by {sort_by} {sort_order} "
        q = q + order_query

    shop_list_raw = Advertisers.objects.raw(q)
    shop_list = list(shop_list_raw)

    rating_list = []
    i = 0
    for item in shop_list:
        rating_query = f"select id,avg(rating) as avg from user_login_user_purchase_list " \
                       f"where company_email = '{item.company_email}' and ad_name='{item.ad_name}' and ad_price='{item.ad_price}' and rating IS NOT NULL"
        avg_rating = tuple(User_Purchase_List.objects.raw(rating_query))
        if not (avg_rating[0].avg):
            avg_rating = -1
        else:
            avg_rating = avg_rating[0].avg
        rating_list.append(avg_rating)
        shop_list[i].rating = "{:.1f}".format(avg_rating)
        i = i+1

    try:
        query2 = f"select id, user_name from user_login_user_purchase_list where user_email = '{user_email}'"
        user_name = tuple(Users.objects.raw(query2))[0]
    except:
        query2 = f"SELECT id, user_name FROM user_signup_users WHERE user_email = '{user_email}' AND user_password = '{user_pass}'"
        user_name = tuple(Users.objects.raw(query2))[0]


    return render(request, 'shop.html', {'user_name': user_name,
                                         'user_email': user_email,
                                         'user_pass': user_pass,
                                         'shop_list': shop_list,
                                         'rating_list':rating_list})
    #return HttpResponse("This is the shop")


def purchase_from_shop(request):
    company_name = request.GET.get('compn')
    ad_name = request.GET.get('adn')
    ad_price = request.GET.get('adp')
    user_email = request.GET.get('email')
    user_name = request.GET.get('name')
    user_pass = request.GET.get('password')
    q = f"select * from company_signup_advertisers where company_name='{company_name}' and ad_name='{ad_name}' and ad_price='{ad_price}'"
    item = Advertisers.objects.raw(q)
    item = item[0]

    check_query = f"select * from user_login_user_purchase_list where company_name='{company_name}' and ad_name='{ad_name}' and ad_price='{ad_price}' and active = '1'"
    check_item = User_Purchase_List.objects.raw(check_query)
    t = tuple(check_item)
    if t!=():
        base_url = "http://127.0.0.1:8000/user_login/shop/not_available"
        query_string = urlencode({'email': user_email, 'password': user_pass})
        url = '{}?{}'.format(base_url, query_string)
        return HttpResponseRedirect(url)

    check_query = f"select * from user_login_user_purchase_list where company_name='{company_name}' and ad_name='{ad_name}' and ad_price='{ad_price}' and user_email='{user_email}'"
    check_item = User_Purchase_List.objects.raw(check_query)
    t = tuple(check_item)

    if t==():
        obj = User_Purchase_List(company_name=item.company_name, company_phone=item.company_phone, company_email=item.company_email,
                                 ad_price=item.ad_price,ad_name=item.ad_name,purchase_date='2002-05-17',user_name=user_name,
                                 user_email=user_email,active=1)
        obj.save()
    else:
        search_id = check_item[0].id
        temp = User_Purchase_List.objects.get(id=search_id)
        temp.active = 1
        temp.save()

    base_url = "http://127.0.0.1:8000/user_login/shop"
    query_string = urlencode({'email': user_email, 'password': user_pass})
    url = '{}?{}'.format(base_url, query_string)
    return HttpResponseRedirect(url)
    #return HttpResponse("This is the purchase area")

def not_available(request):
    user_email = request.GET.get('email')
    user_pass = request.GET.get('password')
    return render(request, 'shop_not_available.html', {'user_pass': user_pass,
                                                        'user_email': user_email,})