from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import requests

# Create your views here.
def index(request):
    context = {'city':"city",'error':False}
    map_context = {'lat': 0, 'lon': 0, 'zoom': 0}
    context.update(map_context)


    return render(request, 'air_quality.html',context)

#def get_air_quality(request, city):
def get_air_quality(request):
    city= None
    if request.method == 'POST':
        city = request.POST.get('city')
    elif request.method == 'GET':
        return HttpResponseRedirect('/')
    # AQICN API endpoint
    endpoint = 'https://api.waqi.info/feed/'

    # Your AQICN API key
    apikey = '7713f48b65c508d66a5a0855aa8cca5c79c58c9c'

    try:
        # Send GET request to AQICN API
        if city != None or city != "":
            response = requests.get(endpoint + city + '/', params={'token': apikey})

        # If the request is successful
        if response.status_code == 200:
            # Parse the response data
            data = response.json()
            air_quality = data['data']['aqi']
            city = city.capitalize()
            lat = data['data']['city']['geo'][0]
            lon = data['data']['city']['geo'][1]
            # Update context variable with air quality and error data
            context = {'air_quality': air_quality,'city':city,'error':False,'lat': lat, 'lon': lon}
            map_context = {'lat': lat, 'lon': lon, 'zoom': 10}
            context = {'air_quality': air_quality,'city':city,'error':False}
            context.update(map_context)
    except:
        #air_quality = 'Invalid city name, please try again with correct city name'
        air_quality = None
        context = {'air_quality': air_quality,'city':city,'error':True}


    # Update context variable with air quality data
    
    # Render the HTML template and pass the context variable to it
    return render(request, 'air_quality.html',context)


def error(request):
    return render(request, 'error.html')