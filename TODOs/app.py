import time

import redis
from flask import Flask,redirect, url_for, request
from datetime import datetime
from influxdb import InfluxDBClient

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


import opentracing
import logging
import time
from jaeger_client import Config


# You can generate a Token from the "Tokens Tab" in the UI
token = "mytoken"
org = "myorg"
bucket = "mybucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379)

log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def init_logger(serv_name):
	config = Config(
		config={
		    'sampler': {
		        'type': 'const',
		        'param': 1,
		    },
		    'local_agent': {
		        'reporting_host': "127.0.0.1",
		        'reporting_port': 5775,
		    },
		    'logging': True,
		},
		service_name=serv_name,
	    )
	return config.initialize_tracer()

tracer = init_logger('/TODOs')


@app.route('/delete_todo',methods = ['GET'])
def deltodo():
	with opentracing.tracer.start_span('Enter /delete_todo') as span:
		span.set_tag('step_1', '1')
	try:		
		tracer.close()	
	except:
		z = 1

	point = Point("endpoint_request").tag("endpoint", "/delete_todo").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)
	if request.method == 'GET':
		opt_task= request.args.get("task")
		opt_red= request.args.get("red")
		if opt_task is None:	
			if opt_red is None:	
				return redirect('http://localhost:5000/main')	
			else:
				return redirect('http://localhost:5000/main')	
		else:
			cache.delete(opt_task)
			if opt_red is None:	
				return redirect('http://localhost:5000/main')	
			else:
				return redirect('http://localhost:5000/main')		
	else:
		return redirect('http://localhost:5000/main')	


@app.route('/add_todo' ,methods = ['GET'])
def addtodo():
	with opentracing.tracer.start_span('Enter /add_todo') as span:
		span.set_tag('step_1', '1')
	try:		
		tracer.close()	
	except:
		z = 1


	point = Point("endpoint_request").tag("endpoint", "/add_todo").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)
	if request.method == 'GET':
		opt_task= request.args.get("task")
		if opt_task is None:	
			return redirect('http://localhost:5000/main')	
		else:
			cache.set(opt_task,1)
			return redirect('http://localhost:5000/main')	
	else:
		return redirect('http://localhost:5000/main')	



@app.route('/get_todo')
def gettodo():
	with opentracing.tracer.start_span('Enter /get_todo') as span:
		span.set_tag('step_1', '1')
	try:		
		tracer.close()	
	except:
		z = 1

	point = Point("endpoint_request").tag("endpoint", "/get_todo").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)
	cacheZv = ""
	for kkv in cache.keys('*'):
		cacheZv = cacheZv + str(kkv.decode("utf-8")) + ","
	return cacheZv

	
        

