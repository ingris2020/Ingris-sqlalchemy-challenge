#########Dependencies#########
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

######Create an app#####
app = Flask(__name__)

####Database Setup#####
engine = create_engine("sqlite:///hawaii.sqlite")

# Create our session link from Python to the DB
session = Session(engine)

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

######Index Route#######
@app.route('/')
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()

    #Jsonify
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)    

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).all()

    temp=  list(np.ravel(results))
    return jsonify(temp)       

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def cal_temp(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        temp = list(np.ravel(results))
        return jsonify(temp)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
        
    temp = list(np.ravel(results))
    return jsonify(temp)


#######Define main behavior##########
if __name__ == "__main__":
    app.run(debug=True)
