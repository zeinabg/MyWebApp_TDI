import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
# def index(request):
#     # return HttpResponse('Hello from Python!')
#     return render(request, "index.html")
# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')
# def index(request):
#     times = int(os.environ.get('TIMES',3))
#     return HttpResponse('Hello! ' * times)

def index(request):
	# api_key = os.environ.get('API_KEY')
	 # input = request.POST
	 # if input:
	 # 	return HttpResponse("I have received your information!")
	return HttpResponse("""
<form id='input' method='get' action='plot'>	
          <p>Ticker symbol: <input type='text' name='symbol' placeholder='GOOG' /></p>
          <p>
          <input type="checkbox" name='features' value='close' />Closing price<br>
          <input type="checkbox" name='features' value='adj_close' />Adjusted closing price<br>
          <input type="checkbox" name='features' value='open' />Opening price<br>
          <input type="checkbox" name='features' value='adj_open' />Adjusted opening price<br>
          </p>
          <p><input type="submit" value="Submit"></p>
          </form>
		""")

def plot(request):
	symbol = request.GET.get('symbol')
	features = request.GET.get('features')
	return HttpResponse("I have received your information: {} {}".format(type(request.GET), dir(request.GET)))


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
