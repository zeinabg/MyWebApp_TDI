import os
import requests
from django.shortcuts import render
from django.http import HttpResponse
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import CDN
from .models import Greeting


def index(request):
	key = os.environ.get('API_KEY')
	return render(request, "form.html")


def plot(request):
	symbol = request.GET.get('symbol')
	features = request.GET.getlist('features')
	return HttpResponse(plotTimeSeries (symbol,features))


def plotTimeSeries (symbol,features):

    # recieve data by Alpha Vantage API in pandas format
    ts = TimeSeries(key='D5RXEJT6U9CLB7QR', output_format='pandas')

    def timeseries_symbol(symbol):
        data, meta_data = ts.get_daily(symbol=symbol , outputsize='compact')
        return data
    data = timeseries_symbol(symbol)
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
       tools="pan,box_zoom,reset,save", title="Alpha Vantage Daily Prices for %s (last 100 days)" % symbol,
       x_axis_label='date', x_axis_type = 'datetime', plot_width=650
    )

    # add some renderers
    if 'open' in features:
        p.line(x, y0, legend_label="open", line_color="blue", line_dash="4 4")
    if 'high' in features:
        p.line(x, y1, legend_label="high", line_color="red")
    if 'low' in features:
        p.line(x, y2, legend_label="low", line_color="black")
    if 'close' in features:
        p.line(x, y2, legend_label="close", line_color="green")

    # show the results
    return file_html(p, CDN)

