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
Measurement = Base.classes.measurement
Station = Base.classes.station
mostRecentDate = ""

########################## Flask ##############################

############## Route - Precipitation by Date ##################

############### Route - Display all Stations ##################

########### Route - Temp Data for Most Active Station #########

############# Route - Temp Data for Given Start Date ##########

############# Route - Temp Data for Given Date Range ##########
