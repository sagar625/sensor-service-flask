from datetime import date, datetime, timedelta
from random import random
import json
from time import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy import sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Sensor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sensorname = db.Column(db.String(50), nullable=False)
	temp = db.Column(db.Float,nullable=False)
	hum=db.Column(db.Float,nullable=False)
	time = db.Column(db.DateTime, default=datetime.utcnow, nullable= False)
	ws = db.Column(db.Float,nullable=False)

	def __init__(self, sensorname, temp, hum, time, ws):
		self.sensorname= sensorname
		self.temp=temp
		self.hum=hum
		self.time=time
		self.ws=ws
		
	def __repr__(self):
		return '<Sensor %r>' % self.id

@app.route('/event', methods=["POST"])
def event():
	event = json.loads(request.data)
	event= Sensor(event["sensorname"],event["temp"],event["hum"],
	toDate(event["time"]), event["ws"])
	db.session.add(event)
	db.session.commit()
	return "posted"

def toDate(dateString): 
    return datetime.strptime(dateString, "%Y/%m/%d %H:%m:%S")


app.run(port=5000, debug=True)	

# @app.route('/search', methods=['GET'])
# def search():
# 	args = request.args
# 	for k,v in args.items():
# 		print(k,v)
# 	query = db.select([db.func.min()])
# def get_bars():
#     with engine.connect() as con:
#         rs = con.execute("SELECT name, license, city, phone, addr FROM bars;")
#         return [dict(row) for row in rs]
	






# db.create_all()
# fake = Faker()
# for _ in range(30):
# 	# transaction_date = fake.date_time_between(1,30)
# 	transaction_date = fake.date_time_between(start_date='-30d',end_date='now')
# 	db.session.add(Sensor(sensorname=fake.random_int(min=1,max=50),temp=fake.random_int(min=0,max=100),hum=fake.random_int(min=0,max=1),
# 	time=transaction_date,ws=fake.random_int(min=0,max=100)))
# db.session.commit()



