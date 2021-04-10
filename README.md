* Run the Project using the command:

docker-compose up -d


* Run the Testing Program:
	
	python TestTaskProject.py <TODO URL> "<Action>" <rate_actions_per_minute>

	- To Create random tasks run the command for example:
		
		
		python TestTaskProject.py localhost:5002 "Create note" 5


	- To Delete random tasks run the command for example:
		
		
		python TestTaskProject.py localhost:5002 "Delete note" 5

