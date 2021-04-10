import sched, time
import sys
import requests 
import random
import string
from random import randrange


if len(sys.argv) != 4:
	print("Number of parameters is not correct!")
	sys.exit(-1)

url = sys.argv[1]
action = sys.argv[2]

def do_task(sc,url,action,rate): 
    for _ in xrange(int(rate)):
 	print("Doing Action")
	if action == "Create note":
		random_str = ''.join(random.choice(string.lowercase) for x in range(randrange(20)))
		urrl = "http://" + url + "/add_todo?task=" + random_str
		requests.get(urrl)
	elif action == "Delete note":
		urrl = "http://" + url + "/get_todo"
		results = requests.get(urrl).content
		res_arr = results.split(",")
		for taskdel in res_arr:
			if taskdel != "":
				urrl = "http://" + url + "/delete_todo?task=" + taskdel
				requests.get(urrl)
				break
    s.enter(60, 1, do_task, (sc,url,action,rate))


if action == "Delete note" or action == "Create note":
	rate = sys.argv[3]
	if rate.isdigit():
		s = sched.scheduler(time.time, time.sleep)
		s.enter(0, 1, do_task, (s,url,action,rate))
		s.run()
	else:
    		print('The rate is not a integer')

	

	
else:
  	print("Action must be Delete note or Create note")
	sys.exit(-1)




