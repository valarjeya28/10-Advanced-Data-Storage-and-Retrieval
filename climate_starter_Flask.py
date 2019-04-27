from datetime import datetime
from datetime import timedelta
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

hello_dict = {}


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Avalable Routes:<br/>"
        f"The dates and precipitation observations from the last year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f" List of stations from the dataset:<br/>"
        f"/api/v1.0/stations<br/>"
        f" List of Temperature Observations (tobs) for the previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"The `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date:<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
     )



@app.route("/api/v1.0/precipitation")
def precipitation():

    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    dictionary_2016_PRCP_results = dict(prcp_results)


    return jsonify(dictionary_2016_PRCP_results)

@app.route('/api/v1.0/stations')

def station():

    # This function returns a list of the  stations 


    list_stations =session.query(Measurement.station,func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by((func.count(Measurement.station)).desc()).all()


    dictionary_Stations = dict(list_stations)
    
    return jsonify(dictionary_Stations)

@app.route('/api/v1.0/tobs')

def tobs():
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    tobs =session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    dictionary_Tobs = dict(tobs)


    return jsonify(dictionary_Tobs)
@app.route('/api/v1.0/<start>')


def tmax_avg_tmin(start=None):

    # The function will output the tavg,tmin,and tmax for dates greater than or equal to input date.

    from_start = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()

    from_start_list=list(from_start)
    return jsonify(from_start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
     
    between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    between_dates_list=list(between_dates)
    return jsonify(between_dates_list)


if __name__ == "__main__":
    app.run(debug=True)