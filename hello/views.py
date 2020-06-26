import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure, output_file, show

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
          <input type="checkbox" name='features' value='open' />Opening price<br>
          <input type="checkbox" name='features' value='high' />High price<br>
          <input type="checkbox" name='features' value='low' />Low price<br>
          <input type="checkbox" name='features' value='close' />Closing price<br>
          </p>
          <p><input type="submit" value="Submit"></p>
          </form>
		""")


def plotTimeSeries (symbol,features):
    
    #recieve data by an API in pandas format
    ts = TimeSeries(key='D5RXEJT6U9CLB7QR', output_format='pandas')
    
    def timeseries_symbol(symbol):
        data, meta_data = ts.get_intraday(symbol=symbol , interval='60min', outputsize='full')
        return data
    data.reset_index(inplace= True)
    
    # prepare data for plot
    x = data['date']
    y0 = data['1. open']
    y1 = data['2. high']
    y2 = data['3. low']
    y3 = data['4. close']

    # output to static HTML file
    output_file("Stock_timeseries.html")

    # create a new plot
    p = figure(
       tools="pan,box_zoom,reset,save", title="Intraday Times Series for ... Stock",
       x_axis_label='date', x_axis_type = 'datetime', plot_width=800
    )

    # add some renderers
    if features[0]:
        p.line(x, y0, legend_label="open", line_color="blue", line_dash="4 4")
    if features[1]:
        p.line(x, y1, legend_label="high", line_color="red")
    if features[2]:
        p.line(x, y2, legend_label="low", line_color="black")
    if features[3]:
        p.line(x, y2, legend_label="close", line_color="green")


    # show the results
    return show(p)

def plot(request):
	symbol = request.GET.get('symbol')
	features = request.GET.getlist('features')
	return HttpResponse(plotTimeSeries (symbol,features))


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
