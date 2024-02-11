from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
#contains the paths to access the different html pages 
# will controls post and get requests from and to db

views = Blueprint('home', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        note = request.form.get('userQuery')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Query is too short!', category='error') 
        else:
            flash('Query made!', category='success')
    
        
    return render_template("index.html")

@views.route('/results')
def vres():
	return render_template("results.html")


