from flask import Flask, Blueprint, render_template, flash, redirect, jsonify, request
from ..gem import basic
import json
import ast
from amadeus import Client, ResponseError, Location
from .flight import Flight
from .metrics import Metrics
from flask import send_file
#contains the paths to access the different html pages 
# will controls post and get requests from and to db


amadeus = Client(client_id='zJhguCjQLJlGA7M2ef1aCLhxOoti9XvA',
    client_secret='ciW4srtGiBlt00D1')

views = Blueprint('home', __name__)

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST': 
        data = request.form.get('userQuery')
        generated_text = basic.generate_details(data)
        flights = flight_offers(generated_text)
        return render_template('results.html', generated_text=generated_text, flights=flights)


def flight_offers(flight_details):
    origin = flight_details.get('Origin')
    destination = flight_details.get('Destination')
    departure_date = flight_details.get('Departuredate')
    return_date = flight_details.get('Returndate')

    kwargs = {'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': 1
            }

    kwargs_metrics = {'originIataCode': origin,
                    'destinationIataCode': destination,
                    'departureDate': departure_date
                    }
    trip_purpose = ''
    try:
        if return_date:
            kwargs['returnDate'] = return_date
            kwargs_trip_purpose = {'originLocationCode': origin,
                                'destinationLocationCode': destination,
                                'departureDate': departure_date,
                                'returnDate': return_date
                                }

            trip_purpose = get_trip_purpose(**kwargs_trip_purpose)
        else:
            kwargs_metrics['oneWay'] = 'true'

        if origin and destination and departure_date:
            flight_offers = get_flight_offers(**kwargs)
            metrics = get_flight_price_metrics(**kwargs_metrics)
            cheapest_flight = get_cheapest_flight_price(flight_offers)
            is_good_deal = ''
            if metrics is not None:
                is_good_deal = rank_cheapest_flight(cheapest_flight, metrics['first'], metrics['third'])
                is_cheapest_flight_out_of_range(cheapest_flight, metrics)

            total = {'flight_offers': flight_offers,
                    'origin': origin,
                    'destination': destination,
                    'departure_date': departure_date,
                    'return_date': return_date,
                    'trip_purpose': trip_purpose,
                    'metrics': metrics,
                    'cheapest_flight': cheapest_flight,
                    'is_good_deal': is_good_deal
                    }
            
            return flight_offers
    except ResponseError as error:
        flash(error.response.result['errors'][0]['detail'], category='error')
    return total


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
"""
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
"""

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return result


