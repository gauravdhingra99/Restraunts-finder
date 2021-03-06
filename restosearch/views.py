from urllib.error import URLError
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.contrib.gis.db.models.functions import Distance
from django.template import RequestContext
from geopy.geocoders.googlev3 import GoogleV3
from geopy.geocoders.googlev3 import GeocoderQueryError
from restosearch import forms
from restosearch import models
from django.shortcuts import render
from .utils import GetRestos
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework.views import APIView
from restosearch.validators import *

def geocode_address(address):
    address = address.encode('utf-8')
    # search(address)
    geocoder = GoogleV3(api_key=settings.GOOGLE_MAP_API_KEY)
    try:
        _, latlon = geocoder.geocode(address)
    except (URLError, GeocoderQueryError, ValueError):
        return None
    else:
        print(latlon)
        return latlon


def get_Restaurants(longitude, latitude,radius):
    current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
    distance_from_point = {'km': radius}
    print(radius)
    # Restaurants = models.Restaurant.objects.filter(
    #     location__distance_lte=(current_point, measure.D(**distance_from_point)))
    # geom = geos.fromstr('POINT(-73 40)')
    Restaurants=models.Restaurant.objects.filter(location__distance_lte=(current_point, measure.D(m=radius))).distinct()
    # print(models.Restaurant.objects.annotate(distance=Distance("location", current_point)).order_by("distance")[0:6])
    print("ktnaaaaaaaa",Restaurants.count())
    # Restaurants = Restaurants[0].location.distance(current_point).order_by('distance')
    # return Restaurants[0].distance(current_point)
    # return models.Restaurant.objects.annotate(distance=Distance("location", current_point)).order_by("distance")
    return Restaurants


def home(request):
    form = forms.AddressForm()
    Restaurants = []
    if request.POST:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = geocode_address(address)
            if location:
                latitude, longitude = location
                Restaurants = get_Restaurants(longitude, latitude)

    return render(request,
                  'home.html',
                  {'form': form, 'Restaurants': Restaurants})

def trys(request):
    return render(request,'base.html')
# from rest_framework.decorators import api_view


from django import template
from django.template.loader import get_template 
from django.template import Context, Template
from django.template.loader import render_to_string

@csrf_exempt
def search(request):
    print(request.method)
    if request.method=='POST':
        print(request.POST)
        lat = request.POST.getlist('user_lat')
        lng = request.POST.getlist('user_long')
        radius = request.POST.getlist('user_radius')
        city = request.POST.getlist('city')

        complete_city_addr=city[0].split(',')
        city=complete_city_addr[0].strip()
        country=complete_city_addr[len(complete_city_addr)-1].strip()
        # print(city,country)

        print("exists karta hai ya nahi",models.Restaurant.objects.filter(city__icontains=city).exists())

        if models.Restaurant.objects.filter(city__icontains=city).exists()==False:
            print("kya huaaaaaaa",Validate.Zomotocity(city,country))
            if Validate.Zomotocity(city,country)==True:            
                GetRestos.searchzomapi(city)
            else:
                GetRestos.searchgoogleapi(city)

        radius=float(radius[0])
        lat,lng=lat[0],lng[0]

        point = Point(float(lng),float(lat))
        restos=get_Restaurants(float(lat),float(lng),radius)
        # restos = models.Restaurant.objects.filter(location__distance_lte=(point, measure.D(m=radius))).values()
        # print("res",restos)

        print(restos.count())

        lst=[]
        for i in restos:
            if i.website=="zomato":
                image=i.data.get('thumb')
                rating=i.data.get("user_rating")['aggregate_rating']
            if i.website=="googlemaps":
                image=""
                rating=i.data.get("rating")
            lst.append({"image":image,"rating":rating,"address":i.address,"name":i.name,"latitude":i.location.x,"longitude":i.location.y})

        return render(request,'Map.html',{"count":restos.count(),'upload_response': lst,"lat":lat,"lon":lng,"city":city,"radius":radius})


def maos(request):
    return render(request,"Map.html")

class SearchRestosView(APIView):
    def post(self,request):
        print(request.data)
        city=request.data.get("city")
        start=request.data.get("start")
        count=request.data.get("count")
        
        if city is None:
            return Response("CITY IS REQUIRED",status=400)        
        
        complete_city_addr=city.split(',')
        city=complete_city_addr[0].strip()
        country=complete_city_addr[len(complete_city_addr)-1].strip()

        if Validate.Zomotocity(city,country)==True:
            flag="zom"
            zomatorestos=models.Restaurant.objects.filter(city__icontains=city,website="zomato")
            if zomatorestos.exists() and zomatorestos.count()>=99:
                data=list(zomatorestos[int(start):int(count)].values('data'))
                return Response({"data":data,"flag":flag,"db":1},status=200)
            else:
                data=GetRestos.searchzomapi(city,start,count)
        else:
            flag="google"
            googlerestos=models.Restaurant.objects.filter(city__icontains=city,website="google")
            print("hai")
            if googlerestos.exists():
                data=list(googlerestos.values('data'))
            else:
                data=GetRestos.searchgoogleapi(city)
        print(flag)
        return Response({"data":data,"flag":flag,"db":0},status=200)









        # resto=models.Restaurant.objects.filter(city__icontains=city)
        # print("exists karta hai ya nahi",models.Restaurant.objects.filter(city__icontains=city).exists())
        # if resto.exists()==False or resto.count()<=99:
        #     print(Validate.Zomotocity())
        #     if Validate.Zomotocity(city,country)==True:
        #         flag='zom'
        #         data=GetRestos.searchzomapi(city,start,count)
        #     else:
        #         flag='google'
        #         data=GetRestos.searchgoogleapi(city)
                        
        # else:
        #     print(resto[int(start):int(count)].count())
        #     if resto.first().website=="zomato":
                
        #         return Response({"data":data,"flag":'zom'},status=200)
        #     else:
                
        #         return Response({"data":data,"flag":"google"},status=200)




        




