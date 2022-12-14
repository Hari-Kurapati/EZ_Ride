import folium
import math
from datetime import date
from django.shortcuts import render,redirect
from . import getroute
from company_signup.models import Advertisers
from user_login.models import User_Purchase_List

pi = 3.141592653589793
Radius = 6378000
ebike_rate = 6/1000      #rupees per Km
bus_rate = 3/1000     #rupees per Km

def showmap(request):
    user_email = request.GET.get('email')
    user_pass = request.GET.get('password')
    user_name = request.GET.get('user_name')
    return render(request,'showmap.html', { 'user_name': user_name,
                                            'user_email': user_email,
                                            'user_pass': user_pass})

def dist_btw_points(long1, lat1, long2, lat2):
    long1 = float(long1)
    lat1 = float(lat1)
    long2 = float(long2)
    lat2 = float(lat2)
    lat1 *= pi / 180
    long1 *= pi / 180
    lat2 *= pi / 180
    long2 *= pi / 180
    #a = math.asin(math.sqrt(math.sin(lat2-lat1)*math.sin(lat2-lat1)/2)) + (math.cos(lat1)*math.cos(lat2)*math.sin((long2-long1)/2)*math.sin((long2-long1)/2))
    a = math.sin((lat2-lat1)/2)*math.sin((lat2-lat1)/2) + (math.cos(lat1)*math.cos(lat2)*math.sin((long2-long1)/2)*math.sin((long2-long1)/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = Radius * c
    return dist

'''
lat3 = 13.012525880757526
long3 = 74.79414148762777
def showroute(request,lat1,long1,lat2,long2):
    figure = folium.Figure(width='60%',height='50%')
    lat1,long1,lat2,long2=float(lat1),float(long1),float(lat2),float(long2)
    route=getroute.get_route(long1,lat1,long3,lat3)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])],
                       zoom_start=12)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='red',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='red')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='play', color='blue')).add_to(m)
    route = getroute.get_route(long3, lat3, long2, lat2)
    folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='blue')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'showroute.html',context)
'''

#'''
def showroute(request,lat1,long1,lat2,long2):
    user_email = request.GET.get('email')
    user_pass = request.GET.get('password')
    user_name = request.GET.get('user_name')

    figure = folium.Figure(width='60%', height='50%')
    route = getroute.get_route(long1, lat1, long2, lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                             (route['start_point'][1])],
                   zoom_start=12)
    m.add_to(figure)
    tot_ebike_dist = 0
    tot_bus_dist = 0
    tot_walk_dist = 0

    lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)
    query = "SELECT * FROM company_signup_advertisers where type IS NOT NULL"
    stops = list(Advertisers.objects.raw(query))
    n = len(stops)
    min_dist = -1
    min_idx = -1
    for i in range(0,n):
        r = dist_btw_points(long1, lat1, stops[i].longitude, stops[i].latitude)
        print(f"dist {i} = {r}")
        if min_dist == -1:
            min_dist = r
            min_idx = i
        elif r < min_dist:
            min_dist = r
            min_idx = i
    print(f"min_idx = {min_idx}")
    print(f"min_idx = {min_idx}")
    print(f"min_idx = {min_idx}")
    print(f"n = {n}")
    print(f"n = {n}")
    route = dist_btw_points(long1,lat1,long2,lat2)
    if(min_dist > route):
        route = getroute.get_route(long1,lat1,long2,lat2)
        tot_walk_dist += route['distance']
        folium.PolyLine(route['route'], weight=8, color='red', opacity=0.6).add_to(m)
        folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='red')).add_to(m)
        folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
        figure.render()
        ebike_cost = tot_ebike_dist * ebike_rate
        ebike_cost = int(ebike_cost*100)/100
        bus_cost = tot_bus_dist * bus_rate
        bus_cost = int(bus_cost*100)/100
        total_cost = ebike_cost + bus_cost
        total_cost = int(total_cost*100)/100
        context = {'map': figure,
                   'walk_dist': tot_walk_dist,
                   'bus_dist': tot_bus_dist,
                   'ebike_dist': tot_ebike_dist,
                   'user_name': user_name,
                   'user_email': user_email,
                   'user_pass': user_pass,
                   'ebike_cost': ebike_cost,
                   'bus_cost': bus_cost,
                   'total_cost': total_cost}
        return render(request, 'showroute.html', context)

    if stops[min_idx].type == "normal stop":
        print("nearest to starting point is a normal stop")
        min_route = getroute.get_route(long1, lat1, stops[min_idx].longitude, stops[min_idx].latitude)
        tot_walk_dist += min_route['distance']
        folium.PolyLine(min_route['route'], weight=8, color='red', opacity=0.6).add_to(m)
        folium.Marker(location=min_route['start_point'], icon=folium.Icon(icon='play', color='red')).add_to(m)
        folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='blue')).add_to(m)

        query = "select * from company_signup_advertisers where type = 'bus stop'"
        bus_stops = list(Advertisers.objects.raw(query))
        long1 = stops[min_idx].longitude
        lat1 = stops[min_idx].latitude
        n = len(bus_stops)
        min_dist = -1
        min_idx = -1
        for i in range(0, n):
            r = dist_btw_points(long1,lat1,bus_stops[i].longitude, bus_stops[i].latitude)
            if min_dist == -1:
                min_dist = r
                min_idx = i
            elif r < min_dist:
                min_dist = r
                min_idx = i

        # This is the nearest bus stop to the end point calculation
        query = "select * from company_signup_advertisers where type = 'bus stop'"
        bus_stops = list(Advertisers.objects.raw(query))
        n = len(bus_stops)
        bus_min_idx = -1
        bus_min_dist = -1
        for i in range(0, n):
            r = dist_btw_points(bus_stops[i].longitude, bus_stops[i].latitude, long2, lat2)
            if bus_min_dist == -1:
                bus_min_dist = r
                bus_min_idx = i
            elif r < bus_min_dist:
                bus_min_dist = r
                bus_min_idx = i

        route = dist_btw_points(long1, lat1, long2, lat2)
        print(f"min_dist = {min_dist}\n  route = {route} \nmin_idx = {min_idx}\nbus_min_idx = {bus_min_idx}")
        if (min_dist > route) or (bus_min_idx == min_idx):
            route = getroute.get_route(long1,lat1,long2,lat2)
            tot_ebike_dist += route['distance']
            folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
            folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='blue')).add_to(m)
            figure.render()
            ebike_cost = tot_ebike_dist * ebike_rate
            ebike_cost = int(ebike_cost * 100) / 100
            bus_cost = tot_bus_dist * bus_rate
            bus_cost = int(bus_cost * 100) / 100
            total_cost = ebike_cost + bus_cost
            total_cost = int(total_cost * 100) / 100
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            d1 = str(d1)
            obj = User_Purchase_List(company_name=bus_stops[bus_min_idx].company_name,
                                     company_email=bus_stops[bus_min_idx].company_email,
                                     ad_price=total_cost, ad_name=d1, purchase_date=today,
                                     active=1, user_name=user_name, user_email=user_email)
            obj.save()
            context = {'map': figure,
                       'walk_dist': tot_walk_dist,
                       'bus_dist': tot_bus_dist,
                       'ebike_dist': tot_ebike_dist,
                       'user_name': user_name,
                       'user_email': user_email,
                       'user_pass': user_pass,
                       'ebike_cost': ebike_cost,
                       'bus_cost': bus_cost,
                       'total_cost': total_cost}
            return render(request, 'showroute.html', context)
        min_route = getroute.get_route(long1,lat1,bus_stops[min_idx].longitude, bus_stops[min_idx].latitude)
        tot_ebike_dist += min_route['distance']
        folium.PolyLine(min_route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
        folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
        long1 = bus_stops[min_idx].longitude
        lat1 = bus_stops[min_idx].latitude



    elif stops[min_idx].type == "bus stop":
        min_route = getroute.get_route(long1, lat1, stops[min_idx].longitude, stops[min_idx].latitude)
        tot_walk_dist += min_route['distance']
        folium.PolyLine(min_route['route'], weight=8, color='red', opacity=0.6).add_to(m)
        folium.Marker(location=min_route['start_point'], icon=folium.Icon(icon='play', color='red')).add_to(m)
        bus_min_idx = min_idx

        ######################################################################################################
        #######################################Part where we check for closest stop from start and end is same
        query = "select * from company_signup_advertisers where type = 'bus stop'"
        bus_stops = list(Advertisers.objects.raw(query))
        n = len(bus_stops)
        min_dist = -1
        min_idx = -1
        for i in range(0, n):
            r = dist_btw_points(long1, lat1, bus_stops[i].longitude, bus_stops[i].latitude)
            if min_dist == -1:
                min_dist = r
                min_idx = i
            elif r < min_dist:
                min_dist = r
                min_idx = i

        # This is the nearest bus stop to the end point calculation
        query = "select * from company_signup_advertisers where type = 'bus stop'"
        bus_stops = list(Advertisers.objects.raw(query))
        n = len(bus_stops)
        bus_min_idx = -1
        bus_min_dist = -1
        for i in range(0, n):
            r = dist_btw_points(bus_stops[i].longitude, bus_stops[i].latitude, long2, lat2)
            if bus_min_dist == -1:
                bus_min_dist = r
                bus_min_idx = i
            elif r < bus_min_dist:
                bus_min_dist = r
                bus_min_idx = i

        long1 = bus_stops[min_idx].longitude
        lat1 = bus_stops[min_idx].latitude
        route = dist_btw_points(long1, lat1, long2, lat2)
        print(f"min_dist = {min_dist}\n  route = {route} \nmin_idx = {min_idx}\nbus_min_idx = {bus_min_idx}")
        if (min_dist > route) or (bus_min_idx == min_idx):
            route = getroute.get_route(long1, lat1, long2, lat2)
            tot_ebike_dist += route['distance']
            folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
            folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='blue')).add_to(m)
            folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='blue')).add_to(m)
            figure.render()
            ebike_cost = tot_ebike_dist * ebike_rate
            ebike_cost = int(ebike_cost * 100) / 100
            bus_cost = tot_bus_dist * bus_rate
            bus_cost = int(bus_cost * 100) / 100
            total_cost = ebike_cost + bus_cost
            total_cost = int(total_cost * 100) / 100
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            d1 = str(d1)
            obj = User_Purchase_List(company_name=bus_stops[bus_min_idx].company_name,
                                     company_email=bus_stops[bus_min_idx].company_email,
                                     ad_price=total_cost, ad_name=d1, purchase_date=today,
                                     active=1, user_name=user_name, user_email=user_email)
            obj.save()
            context = {'map': figure,
                       'walk_dist': tot_walk_dist,
                       'bus_dist': tot_bus_dist,
                       'ebike_dist': tot_ebike_dist,
                       'user_name': user_name,
                       'user_email': user_email,
                       'user_pass': user_pass,
                       'ebike_cost': ebike_cost,
                       'bus_cost': bus_cost,
                       'total_cost': total_cost}
            return render(request, 'showroute.html', context)
        ######################################################################################################
        ######################################################################################################

        folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
        long1 = stops[bus_min_idx].longitude
        lat1 = stops[bus_min_idx].latitude

    query = "select * from company_signup_advertisers where type = 'bus stop'"
    bus_stops = list(Advertisers.objects.raw(query))
    n = len(bus_stops)
    min_idx = -1
    min_dist = -1
    for i in range(0,n):
        r = dist_btw_points(bus_stops[i].longitude, bus_stops[i].latitude,long2,lat2)
        if min_dist == -1:
            min_dist = r
            min_idx = i
        elif r < min_dist:
            min_dist = r
            min_idx = i
    bus_route = getroute.get_route(long1,lat1,bus_stops[min_idx].longitude,bus_stops[min_idx].latitude)
    tot_bus_dist += bus_route['distance']
    folium.PolyLine(bus_route['route'], weight=8, color='green', opacity=0.6).add_to(m)
    folium.Marker(location=bus_route['end_point'], icon=folium.Icon(icon='play', color='blue')).add_to(m)

    ebike_route = getroute.get_route(bus_stops[min_idx].longitude, bus_stops[min_idx].latitude,long2,lat2)
    tot_ebike_dist += ebike_route['distance']
    folium.PolyLine(ebike_route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    folium.Marker(location=ebike_route['end_point'], icon=folium.Icon(icon='stop', color='blue')).add_to(m)

    figure.render()
    ebike_cost = tot_ebike_dist * ebike_rate
    ebike_cost = int(ebike_cost * 100) / 100
    bus_cost = tot_bus_dist * bus_rate
    bus_cost = int(bus_cost * 100) / 100
    total_cost = ebike_cost + bus_cost
    total_cost = int(total_cost * 100) / 100
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    d1 = str(d1)
    obj = User_Purchase_List(company_name=bus_stops[min_idx].company_name,
                             company_email=bus_stops[min_idx].company_email,
                             ad_price=total_cost, ad_name=d1, purchase_date=today,
                             active=1, user_name=user_name, user_email=user_email)
    obj.save()
    context = {'map': figure,
               'walk_dist': tot_walk_dist,
               'bus_dist': tot_bus_dist,
               'ebike_dist': tot_ebike_dist,
               'user_name': user_name,
               'user_email': user_email,
               'user_pass': user_pass,
               'ebike_cost': ebike_cost,
               'bus_cost': bus_cost,
               'total_cost': total_cost}
    return render(request, 'showroute.html', context)
#'''

'''
def showroute(request,lat1,long1,lat2,long2):
    figure = folium.Figure(width='60%',height='50%')
    lat1,long1,lat2,long2=float(lat1),float(long1),float(lat2),float(long2)
    route=getroute.get_route(long1,lat1,long2,lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])], 
                       zoom_start=12)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'showroute.html',context)


def showroute(request,lat1,long1,lat2,long2):
    figure = folium.Figure(width='60%', height='50%')
    route = getroute.get_route(long1, lat1, long2, lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                             (route['start_point'][1])],
                   zoom_start=12)
    m.add_to(figure)
    tot_ebike_dist = 0
    tot_bus_dist = 0
    tot_walk_dist = 0

    lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)
    query = "SELECT * FROM company_signup_advertisers where type IS NOT NULL"
    stops = list(Advertisers.objects.raw(query))
    n = len(stops)
    min_dist = -1
    for i in range(0,n):
        r = getroute.get_route(long1, lat1, stops[i].longitude, stops[i].latitude)
        if min_dist == -1:
            min_dist = r['distance']
        elif r['distance'] < min_dist:
            min_dist = r['distance']
            min_route = r
            min_idx = i

    route = getroute.get_route(long1,lat1,long2,lat2)
    if(min_dist > route['distance']):
        folium.PolyLine(route['route'], weight=8, color='red', opacity=0.6).add_to(m)
        folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='red')).add_to(m)
        folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
        figure.render()
        context = {'map': figure,
                   'walk_dist': tot_walk_dist,
                   'bus_dist': tot_bus_dist,
                   'ebike_dist': tot_ebike_dist}
        return render(request, 'showroute.html', context)

    if stops[min_idx].type == "normal stop":
        tot_walk_dist += min_route['distance']
        folium.PolyLine(min_route['route'], weight=8, color='red', opacity=0.6).add_to(m)
        folium.Marker(location=min_route['start_point'], icon=folium.Icon(icon='play', color='red')).add_to(m)
        folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='blue')).add_to(m)

        query = "select * from company_signup_advertisers where type = 'bus stop'"
        bus_stops = list(Advertisers.objects.raw(query))
        long1 = stops[min_idx].longitude
        lat1 = stops[min_idx].latitude
        n = len(bus_stops)
        min_dist = -1
        for i in range(0, n):
            r = getroute.get_route(long1,lat1,bus_stops[i].longitude, bus_stops[i].latitude)
            if min_dist == -1:
                min_dist = r['distance']
            elif r['distance'] < min_dist:
                min_dist = r['distance']
                min_route = r
                min_idx = i
        route = getroute.get_route(long1,lat1,long2.lat2)
        if min_dist > route['distance']:
            folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
            folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='blue')).add_to(m)
            figure.render()
            context = {'map': figure,
                       'walk_dist': tot_walk_dist,
                       'bus_dist': tot_bus_dist,
                       'ebike_dist': tot_ebike_dist}
            return render(request, 'showroute.html', context)

        folium.PolyLine(min_route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
        folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)



    elif stops[min_idx].type == "bus stop":
        tot_walk_dist += min_route['distance']
        folium.PolyLine(min_route['route'], weight=8, color='red', opacity=0.6).add_to(m)
        folium.Marker(location=min_route['start_point'], icon=folium.Icon(icon='play', color='red')).add_to(m)
        folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)

    query = "select * from company_signup_advertisers where type = 'bus stop'"
    bus_stops = list(Advertisers.objects.raw(query))
    long1 = stops[min_idx].longitude
    lat1 = stops[i].latitude
    n = len(bus_stops)
    min_dist = -1
    for i in range(0,n):
        r = getroute.get_route(bus_stops[i].longitude, bus_stops[i].latitude,long2,lat2)
        if min_dist == -1:
            min_dist = r['distance']
        elif r['distance'] < min_dist:
            min_dist = r['distance']
            min_route = r
            min_idx = i
    bus_route = getroute.get_route(long1,lat1,bus_stops[min_idx].longitude,bus_stops[min_idx].latitude)
    tot_bus_dist += bus_route['distance']
    folium.PolyLine(bus_route['route'], weight=8, color='green', opacity=0.6).add_to(m)
    folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='play', color='blue')).add_to(m)

    ebike_route = getroute.get_route(bus_stops[i].longitude, bus_stops[i].latitude,long2,lat2)
    tot_ebike_dist += ebike_route['distance']
    folium.PolyLine(ebike_route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    folium.Marker(location=min_route['end_point'], icon=folium.Icon(icon='stop', color='blue')).add_to(m)

    figure.render()
    context = {'map': figure,
               'walk_dist': tot_walk_dist,
               'bus_dist': tot_bus_dist,
               'ebike_dist': tot_ebike_dist}
    return render(request, 'showroute.html', context)

'''
