from __future__ import print_function
import sys
import redis
import requests
from flask import Flask,redirect, url_for, request,session
from datetime import datetime
from influxdb import InfluxDBClient
import opentracing
import logging
import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import logging
from jaeger_client import Config


# You can generate a Token from the "Tokens Tab" in the UI
token = "mytoken"
org = "myorg"
bucket = "mybucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)



app = Flask(__name__)
app.secret_key = 'fafafaf2525252525252525d'
app.config['SESSION_TYPE'] = 'filesystem'
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

tracer = init_logger('FrontEnd')

@app.route('/main')
def mainPanel():
	with opentracing.tracer.start_span('Enter Main') as span:
		span.set_tag('step', '1')

	

	point = Point("endpoint_request").tag("endpoint", "/main").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)

	if 'can_login' not in session:
		time.sleep(2)
		try:		
			tracer.close()	
		except:
			z = 1		
		return redirect('/')
	else: 
		add_keys_str = ""		
		count_keyszz = len(cache.keys('*'))	
		for kkv in cache.keys('*'):
			add_keys_str = add_keys_str + '<li><span class="vt">' + str(kkv.decode("utf-8")) + '</span><span class="close">&times;</span></li>'  
		time.sleep(2)
		try:		
			tracer.close()	
		except:
			z = 1	
		return """

	<!DOCTYPE html>
<html lang="en">
<head>
<title>Panel</title>
<style>


ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

ul li {
  border: 1px solid #ddd;
  margin-top: -1px; /* Prevent double borders */
  background-color: white;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: block;
  position: relative;
}



.close {
  cursor: pointer;
  position: absolute;
  top: 50%;
  background-color: red;
  right: 0%;
  padding: 12px 16px;
  transform: translate(0%, -50%);
}

header {
  background-color: black;
  padding: 2px;

  font-size: 15px;
  color: white;
}



.buttonred {
  background-color: red;
  border: none;
  color: white;
  padding: 5px 5px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

.buttongreen {
  background-color: green;
  border: none;
  color: white;
  padding: 5px 5px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}


/* Style the footer */
footer {
  background-color: black;
  padding: 1px;
  text-align: center;
  color: white;
}


</style>
</head>
<body>

<header>
	<table  style="width:100%"><tr><td style="padding-left: 2%;text-align:left;width:50%">test1<button class="buttongreen" style="margin-left:2%;">Admin</button></td><td style="padding-right: 2%;text-align:right;width:50%"><button  onclick="location.href='/do_LogOut'" class="buttonred">Logout</button></td></tr></table>
</header>

<section>
 
<h2>TODOs (""" + str(count_keyszz) + """)</h2>

<form  method="get" action="http://localhost:5002/add_todo">
  <label for="task">ADD Task:</label><br>
  <input type="text" id="task" name="task" ><br>
  <input style="background-color:lightgreen;" type="submit" value="ADD Task">
</form> 
<br>
<br>

<ul>
  """ + add_keys_str + """

</ul>

<script>
var closebtns = document.getElementsByClassName("close");
var i;

for (i = 0; i < closebtns.length; i++) {
  closebtns[i].addEventListener("click", function() {
    ToDel = this.parentElement.getElementsByClassName("vt")[0].innerText;
	window.location.href = "http://localhost:5002/delete_todo?red=1&task=" + ToDel;
	 

    this.parentElement.style.display = 'none';
    
  });
}
</script>
</section>



</body>
</html>



	   """	


@app.route('/do_LogOut')
def ProcessLogOut():
	with opentracing.tracer.start_span('Enter do_LogOut') as span:
		span.set_tag('step_1', '1')

	point = Point("endpoint_request").tag("endpoint", "/do_LogOut").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)
	del session['can_login']
	try:		
		tracer.close()	
	except:
		z = 1
	return redirect('/')


@app.route('/do_Auth',methods = ['POST'])
def ProcessLogin():
	with opentracing.tracer.start_span('Enter do_Auth') as span:
		span.set_tag('step_1', '1')

	point = Point("endpoint_request").tag("endpoint", "/do_Auth").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)
	if request.method == 'POST':
		if "passi" in request.form and "useri" in request.form:
			with opentracing.tracer.start_span('Enter do_Auth req') as span:
				span.set_tag('step_2', '1')
			msg = requests.get('http://localhost:5001/users?name=' + request.form["useri"] + "&pass="  + request.form["passi"] ).content
			with opentracing.tracer.start_span('Enter do_Auth req end') as span:
				span.set_tag('step_3', '1')
			try:		
				tracer.close()	
			except:
				z = 1			
			if str(msg) == "b'good'":
				session['can_login'] = 1
				return redirect('/main')		
			return redirect('/')	
		else:
			try:		
				tracer.close()	
			except:
				z = 1	
			return redirect('/')
	else:
		try:		
			tracer.close()	
		except:
			z = 1	
		return redirect('/')

@app.route('/')
def LoginPanel():
	with opentracing.tracer.start_span('Enter /home') as span:
		span.set_tag('step_1', '1')

	point = Point("endpoint_request").tag("endpoint", "/").field("value", 1).time(datetime.utcnow(), WritePrecision.NS)

	write_api.write(bucket, org, point)
	try:		
		tracer.close()	
	except:
		z = 1
	return """

	<!DOCTYPE html>
<html lang="en">
<head>
<title>Panel</title>
<style>


header {
  background-color: black;
  padding: 2px;

  font-size: 15px;
  color: white;
}



.buttonred {
  background-color: red;
  border: none;
  color: white;
  padding: 5px 5px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

.buttongreen {
  background-color: green;
  border: none;
  color: white;
  padding: 5px 5px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}


/* Style the footer */
footer {
  background-color: black;
  padding: 1px;
  text-align: center;
  color: white;
}


</style>
</head>
<body>

<header>
	<table  style="width:100%"><tr><td style="padding-left: 2%;text-align:left;width:50%">test1</td><td style="padding-right: 2%;text-align:right;width:50%"><button class="buttongreen">Login</button></td></tr></table>
</header>

<section>
 <div style="text-align:center;"><h4>Please Login</h4><br><form  method="post" action="/do_Auth"><input type="text" id="user" name="useri"><br><br><input type="text" id="pass" name="passi"><br><br><input type="submit" style="background-color:lightgreen;"  value="Login"></form><br><br></div>
</section>

<footer>

</footer>

</body>
</html>



	   """


