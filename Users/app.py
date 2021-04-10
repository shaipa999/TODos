from __future__ import print_function
import sys
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

tracer = init_logger('/users')

@app.route('/users',methods = ['GET'])
def ProcessLogin():
	
	with opentracing.tracer.start_span('Enter /users') as span:
		span.set_tag('step_1', '1')
	try:		
		tracer.close()	
	except:
		z = 1
	point = Point("endpoint_request").tag("endpoint", "/users").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)
	if request.method == 'GET':
		opt_name= request.args.get("name")
		opt_pass = request.args.get("pass")
		if opt_name is None or opt_pass is None:
			
					
			return "badz"
		else:
			if opt_name == "johnd" and opt_pass == "foo":
				return "good"
			else:
				return "bad"
	else:
		return "bad"

