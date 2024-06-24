from flask import Flask, Blueprint, render_template, flash, redirect, jsonify, request
from .generator import generate_details
import json
import ast
from flask import send_file
import requests
from .flight import Flight
from amadeus import Client, ResponseError

##api setup for flights data
amadeus = Client(
    client_id='CLIENT_API_KEY',
    client_secret='CLIENT_SECRET'
)


views = Blueprint('home', __name__)
##renders homepage
@views.route('/')
def home():
    return render_template("index.html")
#renders flight results page
@views.route('/results')
def results():
    return render_template("results.html")
    
##calls function using google gemini generative ai tools to perform NLP of user input
@views.route('/', methods=['POST'])
def fly():
    if request.method == 'POST': 
        data = request.form.get('userQuery')
        flight_details = generate_details(data)
        print(flight_details)
        flights = flight_offers(flight_details)  
        if flights != []:
            return render_template('results.html', flights=flights)
    return render_template('results.html')

##calls amadeus api to return the available flights given a valid user prompt
def flight_offers(flight_details):

    origin = flight_details.get('Origin')
    destination = flight_details.get('Destination')
    departure_date = flight_details.get('DepartureDate')
    return_date = flight_details.get('ReturnDate')
    
    params = {
    'originLocationCode': origin,
    'destinationLocationCode': destination,
    'departureDate': departure_date,
    'currencyCode': 'USD',
    'adults': 1,
    'max': 10,  # Maximum number of flight offers to return
    }
    if return_date:
        params["returnDate"] = return_date
        
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
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
    
        return returned_flights
    return []
