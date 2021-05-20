from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///hawaii2.sqlite")

session = Session(engine)

app = Flask(__name__)

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station= Base.classes.station


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
       
        one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        Prcp = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date > one_year).all()
        session.close()
        prcp_list = dict(Prcp)
        return jsonify(prcp_list)
@app.route("/api/v1.0/stations")
def stations():
        station_qry = session.query(Station.station, Station.name).all()
        Stations = list(station_qry)
        return jsonify(Stations)
@app.route("/api/v1.0/tobs")
def tobs():
        yr = dt.date(2017,8,23) - dt.timedelta(days=365)
        Tobs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date > yr).all()
        session.close()
        tobs_dict = list(Tobs)
        return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def startday(start):
        starter = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        session.close()
        start_dict = list(starter)
        return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
        startend = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        session.close()
        start_end_dict = list(startend)
        return jsonify(start_end_dict)

if __name__ == '__main__':
    app.run(debug=True)