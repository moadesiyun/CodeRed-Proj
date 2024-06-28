from flask import Flask, Blueprint, render_template, flash, redirect, jsonify, request
from .generator import generate_details
import json
import ast
from flask import send_file
import requests
from .flight import Flight
from amadeus import Client, ResponseError

amadeus = Client(
    client_id='D8Hvx5G6n69b9S5lIG2v9OKe6kMEyA5W',
    client_secret='A42ICQFWlG4YGmGy'
)

API_KEY = 'D8Hvx5G6n69b9S5lIG2v9OKe6kMEyA5W'
API_URL = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

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
        print(flight_details)
        flights, route = flight_offers(flight_details)  
        if flights != []:
            print(flights[0])
            return render_template('results.html', flights=flights, route = route)
        
    return render_template('results.html')
    

def flight_offers(flight_details):

    origin = flight_details.get('Origin')
    destination = flight_details.get('Destination')
    departure_date , return_date = '', ''
    if flight_details.get('Departuredate'):
        departure_date = flight_details.get('Departuredate') 
        return_date = flight_details.get('Returndate')
    else:
        departure_date = flight_details.get('DepartureDate') 
        return_date = flight_details.get('ReturnDate')
    
    params = {
    'originLocationCode': origin,
    'destinationLocationCode': destination,
    'departureDate': departure_date,
    'currencyCode': 'USD',
    'adults': 1# Maximum number of flight offers to return
    }
    if return_date:
        params["returnDate"] = return_date
    path = params
    print(origin," ",destination,' ',departure_date)
    returned_flights = []
    if origin and destination and departure_date:
        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**params)
        except ResponseError as error:
            print("this is error code:", error, error.response.result["errors"][0]["detail"])
            return render_template("index.html")
            
        for flight in search_flights.data:
            offer = Flight(flight).construct_flights()
            returned_flights.append(offer)
        
        return returned_flights, path
    return [], path
