import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

app=Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>" 
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    list_prcp=[]
    for date,prcp in results:
        prcp_dict={}
        prcp_dict[date]=prcp
        list_prcp.append(prcp_dict)

    return jsonify(list_prcp)

@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    station_results=session.query(Station.station).all()
    session.close()
    stations_list=[]
    for station in station_results:
        stations_list.append(list(station))
    return jsonify(stations_list)  

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs_results=session.query(Measurement.tobs).\
        filter((Measurement.station=='USC00519281')&(Measurement.date>='2016-08-23')&(Measurement.date<='2017-08-23')).\
        all()
    tobs_results_show=list(np.ravel(tobs_results))
    session.close()
    return jsonify(tobs_results_show)

@app.route("/api/v1.0/<start>")
def start_tobs(start):
    session=Session(engine)
    stats_start=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).first()
    session.close()
    return jsonify(list(stats_start))

@app.route("/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_by_start_end(start_date,end_date):
    session = Session(engine)
    time_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter((Measurement.date >= start_date)&(Measurement.date <= end_date)).first()
    session.close()
    return jsonify(list(time_stats))

if __name__ == "__main__":
    app.run(debug=True)
