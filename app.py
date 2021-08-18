# Add dependencies and assign them aliases: 
import datetime as dt
import numpy as np
import pandas as pd

# the dependencies we need for SQLAlchemy, which will help us access our data in the SQLite database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# add the code to import the dependencies that we need for Flask
from flask import Flask, jsonify

# set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Now let's reflect the database into our classes
Base = automap_base()

# reflect our tables
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database 
session = Session(engine)

# Set Up Flask
# define our Flask app. This will create a Flask application called "app."
app = Flask(__name__)
# All of your routes should go after the app = Flask(__name__) line of code. 
# Otherwise, your code may not run properly.

# We can define the welcome route using the code: 
@app.route("/")  # Then you put your function below this
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! 
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. 
# This convention signifies that this is version 1 of our application. This line can be updated to 
# support future versions of the app as well.
# Flask result: http://127.0.0.1:5000/

# Create precipitation route
# Every time you create a new route, your code should be aligned to the left in order to avoid errors.
#@app.route("/api/v1.0/precipitation")
#def precipitation():  
    #return
#  This was just to show the base form of how to do this.  We also want to add the line of code that
#  calculates the date one year ago from the most recent date in the databaseThe full code is:
#@app.route("/api/v1.0/precipitation")
#def precipitation():
   #prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   #return
# We also need to write a query to get the date and precipitation for the previous year:
#@app.route("/api/v1.0/precipitation")
#def precipitation():
   #prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   #precipitation = session.query(Measurement.date, Measurement.prcp).\
      #filter(Measurement.date >= prev_year).all()
   #return
# Finally, we'll create a dictionary with the date as the key and the precipitation as the value.
#  To do this, we will "jsonify" our dictionary. Jsonify() is a function that converts the dictionary
#  to a JSON file. We'll use jsonify() to format our results into a JSON structured file
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# To navigate to this we add the base url that is created with flask run in the command line:
# http://127.0.0.1:5000/
# Then add the new route which is:
# api/v1.0/precipitation

# Create stations route
# Do not indent this, it should be all the way to the left.
@app.route("/api/v1.0/stations")
# With our route defined, we'll create a new function called stations()
#def stations():
    #return
# Now we need to create a query that will allow us to get all of the stations in our database
#def stations():
    #results = session.query(Station.station).all()
    #return
#We want to start by unraveling our results into a one-dimensional array. To do this, we want to use thefunction np.ravel(), with results as our parameter.
# Next, we will convert our unraveled results into a list. To convert the results to a list, we will
#  need to use the list function, which is list(), and then convert that array into a list. Then we'll 
# jsonify the list and return it as JSON. Let's add that functionality to our code
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# You may notice here that to return our list as JSON, we need to add stations=stations. This 
# formats our list into JSON.
# This route is: http://127.0.0.1:5000/api/v1.0/stations

# Monthly Temperature route
# For this route, the goal is to return the temperature observations for the previous year. 
# As with the previous routes, begin by defining the route
@app.route("/api/v1.0/tobs")
# Next, create a function called temp_monthly()
#def temp_monthly():
    #return
# Now, calculate the date one year ago from the last date in the database.
#def temp_monthly():
    #prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #return
# The next step is to query the primary station for all the temperature observations from the previous year. 
#def temp_monthly():
    #prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #results = session.query(Measurement.tobs).\
        #filter(Measurement.station == 'USC00519281').\
        #filter(Measurement.date >= prev_year).all()
    #return
# Finally, as before, unravel the results into a one-dimensional array and convert that array into a list. 
# Then jsonify the list and return our results
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# Results: http://127.0.0.1:5000/api/v1.0/tobs

# Create statistics route
# Our last route will be to report on the minimum, average, and maximum temperatures. 
# However, this route is different from the previous ones in that we will have to provide both a 
# starting and ending date. So we will need two beginnings 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Next, create a function called stats() to put our code in.
#def stats():
     #return
# We need to add parameters to our stats()function: a start parameter and an end parameter. 
# For now, set them both to None
#def stats(start=None, end=None):
     #return
# With the function declared, we can now create a query to select the minimum, average, and maximum 
# temperatures from our SQLite database. We'll start by just creating a list called sel
#def stats(start=None, end=None):
    #sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
# Since we need to determine the starting and ending date, add an if-not statement to our code. 
# This will help us accomplish a few things. We'll need to query our database using the list that we
#  just made. Then, we'll unravel the results into a one-dimensional array and convert them to a list. 
# Finally, we will jsonify our results and return them
# In the following code, take note of the asterisk in the query next to the sel list.
#  Here the asterisk is used to indicate there will be multiple results for 
# our query: minimum, average, and maximum temperatures.
#def stats(start=None, end=None):
    #sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #if not end:
        #results = session.query(*sel).\
            #filter(Measurement.date >= start).all()
        #temps = list(np.ravel(results))
        #return jsonify(temps=temps)
# Now we need to calculate the temperature minimum, average, and maximum with the start and end dates. 
# We'll use the sel list, which is simply the data points we need to collect. Let's create our next query,
#  which will get our statistics data.
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Results: http://127.0.0.1:5000/api/v1.0/temp/start/endroute
# This will get us a not found.  We need to add a starte and end date. Ex
# http://127.0.0.1:5000/api/v1.0/temp/2017-06-01/2017-06-30

