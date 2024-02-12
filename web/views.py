from flask import Flask, Blueprint, render_template, flash, redirect, jsonify, request
from .generator import generate_details
import json
import ast
from amadeus import Client, ResponseError
from flask import send_file
import requests

#contains the paths to access the different html pages 
# will controls post and get requests from and to db
token = 'AMADEUS_AGENT_TOKEN'
headers={'Authorization': 'Bearer' + token}


views = Blueprint('home', __name__)

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/results')
def results():
    return render_template("results.html")

@views.route('/', methods=['POST'])
def fly():
    if request.method == 'POST': 
        data = request.form.get('userQuery')
        flight_details = generate_details(data)
        flights = flight_offers(flight_details)  
        return render_template('results.html', flights=flights)


def flight_offers(flight_details):
    try:
        origin = flight_details.get('Origin')
        destination = flight_details.get('Destination')
        departure_date = flight_details.get('Departuredate')
        return_date = flight_details.get('Returndate')
        
        kwargs = {'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'adults': 1
                }
        # if return_date:
        #     kwargs['returnDate'] = return_date
        address = 'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode='+str(origin)+'&destinationLocationCode='+str(destination)+"&departureDate="+str(departure_date)+'&adults=1&nonStop=false&max=250'
        res = requests.get(address, headers=headers)
        offers = res.json()['data']
        
        print(offers)
        return offers
        
    except ResponseError as e:
        print(e)
        return []  

""""
def get_flight_offers(**kwargs):
    search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
    flight_offers = []
    for flight in search_flights.data:
        offer = Flight(flight).construct_flights()
        flight_offers.append(offer)
    return flight_offers


def get_flight_price_metrics(**kwargs_metrics):
    kwargs_metrics['currencyCode'] = 'USD'
    metrics = amadeus.analytics.itinerary_price_metrics.get(**kwargs_metrics)
    return Metrics(metrics.data).construct_metrics()


def get_trip_purpose(**kwargs_trip_purpose):
    trip_purpose = amadeus.travel.predictions.trip_purpose.get(**kwargs_trip_purpose).data
    return trip_purpose['result']


def get_cheapest_flight_price(flight_offers):
    return flight_offers[0]['price']


def rank_cheapest_flight(cheapest_flight_price, first_price, third_price):
    cheapest_flight_price_to_number = float(cheapest_flight_price)
    first_price_to_number = float(first_price)
    third_price_to_number = float(third_price)
    if cheapest_flight_price_to_number < first_price_to_number:
        return 'A GOOD DEAL'
    elif cheapest_flight_price_to_number > third_price_to_number:
        return 'HIGH'
    else:
        return 'TYPICAL'


def is_cheapest_flight_out_of_range(cheapest_flight_price, metrics):
    min_price = float(metrics['min'])
    max_price = float(metrics['max'])
    cheapest_flight_price_to_number = float(cheapest_flight_price)
    if cheapest_flight_price_to_number < min_price:
        metrics['min'] = cheapest_flight_price
    elif cheapest_flight_price_to_number > max_price:
        metrics['max'] = cheapest_flight_price

@views.route('/', methods=['GET', 'POST'])
def origin_airport_search():
    if request.is_xhr():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
            return jsonify(get_city_airport_list(data))
        except ResponseError as error:
            flash(error.response.result['errors'][0]['detail'], category='error')
            return jsonify([])

@views.route('/', methods=['GET', 'POST'])
def destination_airport_search():
    if request.is_xhr():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
            return jsonify(get_city_airport_list(data))
        except ResponseError as error:
            flash(error.response.result['errors'][0]['detail'], category='error')
            return jsonify([])


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return result


"""
