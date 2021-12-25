# sqalchemy imports
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

# flask imports
from flask import Flask, jsonify

# other python package imports
import numpy as np
import pandas as pd
import datetime as dt

###################### Database Setup #########################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect and existing database
Base = automap_base()
#Refelct the tables
Base.prepare(engine, reflect = True)

#Save the refrences to the tables
measurements = Base.classes.measurement
theStations = Base.classes.station
mostRecentDate = ""

########################## Flask ##############################

app = Flask(__name__)

##################### Route - Home ############################
@app.route('/')
def index():

    return (
        f'<h1>Available Routes for this Climate App</h1><br>'
        f'<ul><li> /api/v1.0/precipitation </li><br>'
        f'<li> /api/v1.0/stations </li><br>'
        f'<li> /api/v1.0/tobs </li><br>'
        f'<li> /api/v1.0/<start> </li><br>'
        f'<li> /api/v1.0/<start>/<end> </li></ul><br>'
        )

############## Route - Precipitation by Date ##################
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Start the session
    session = Session(engine)

    # Find the most recent date and the date one year earlier
    latestDate = session.query(measurements.date).order_by(measurements.date.desc()).first()
    queryDate = dt.date.fromisoformat(latestDate.date) - dt.timedelta(days=365)

    # Query for the precipitation data
    precipData = session.query(measurements.prcp, measurements.date).\
        filter(measurements.date > queryDate).order_by(measurements.date.desc())

    session.close()

    # Create dictionary, return jsonified version
    precipList = []
    for dataPoint, date in precipData:
        precipDict = {
            'Date': date,
            'Precipitation': dataPoint
        }
        precipList.append(precipDict)
    return jsonify(precipList)

############### Route - Display all stationss ##################
@app.route('/api/v1.0/stations')
def stations():
    # Start the session
    session = Session(engine)

    # Query for the stations
    stationsList = [] 
    theseStations = session.query(theStations.station,theStations.name).distinct().all()

    session.close()

    for station in theseStations:
        stationDict = {
            'Station ID': station.station,
            'Station Name': station.name
        }
        stationsList.append(stationDict)
    return jsonify(stationsList)

########### Route - Temp Data for Most Active stations #########
@app.route('/api/v1.0/tobs')
def tobs():
    # Start the session
    session = Session(engine)

    # Query to find the most active station
    aCount = func.count('*').label('count')
    stationsByActivity = session.query(aCount, measurements.station).\
        group_by(measurements.station).order_by(aCount.desc())
    mostActiveStation = stationsByActivity.all()[0][1]

    # Query for the most active station's temp data for the previous year
    # Find the most recent date and the date one year earlier
    latestDate = session.query(measurements.date).order_by(measurements.date.desc()).first()
    queryDate = dt.date.fromisoformat(latestDate.date) - dt.timedelta(days=365)
    activeStationTempData = session.query(measurements.date, measurements.tobs).\
        filter(measurements.station == mostActiveStation).\
        filter(measurements.date > queryDate).all()
    
    session.close()

    tobsList = []
    for date, tobs in activeStationTempData:
        tobsDict = {
            'Date': date,
            'Temperature': tobs
        }
        tobsList.append(tobsDict)

    return jsonify(tobsList)

############# Route - Temp Data for Given Start Date ###########
@app.route("/api/v1.0/<start>")
def start_temp(start):
    # Create the session
    session = Session(engine)

    # set up min avg and max functions
    selection = [func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)]

    # Query for the temperatures since the start date
    tempInfo = session.query(*selection).filter(measurements.date >= start).all()
    tempInfoList = list(np.ravel(tempInfo))

    session.close()

    tempInfoDict = {
        'Minimum Observed Temperature': tempInfoList[0],
        'Average Observed Temperature': round(tempInfoList[1], 1),
        'Maximum Observed Temperature': tempInfoList[2]
    }
    
    return jsonify(tempInfoDict)

############# Route - Temp Data for Given Date Range ###########
@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    # Create the session
    session = Session(engine)

    # set up min avg and max functions
    selection = [func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)]

    # Query for the temperatures since the start date
    tempInfo = session.query(*selection).filter(measurements.date >= start).filter(measurements.date <= end).all()
    tempInfoList = list(np.ravel(tempInfo))

    session.close()

    tempInfoDict = {
        'Minimum Observed Temperature': tempInfoList[0],
        'Average Observed Temperature': round(tempInfoList[1], 1),
        'Maximum Observed Temperature': tempInfoList[2]
    }
    
    return jsonify(tempInfoDict)


if __name__ == "__main__":
    app.run(debug=True)