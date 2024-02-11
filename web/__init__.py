from flask import Flask
#this file creates paths for the different route we will run

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'codered proj'
    from .views import views
    #register blueprint creates 
    app.register_blueprint(views, url_prefix='/')
    
    
    return app
