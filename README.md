# RoutePlanner


*** 

### Project Member:
* [Austin Miller](mailto:austin.j07.miller@wmich.edu)
* [Bjarne Wilken](mailto:bjarne.wilken@wmich.edu)
* [Christian Fuentes](mailto:cdd9168@wmich.edu)
* [Matthew Phillips](mailto:matthew.a.phillips@wmich.edu)
* [Mike Henke](mailto:mgs8776@wmich.edu)


***

### Abstract:
Kalamazoo Route Planner is a website that calculates routes based on user inputs and preferences. 
The website utilizes common front-end technologies like JavaScript and HTML. 

The back end uses Python and other libraries, like Flask, to run the site and store data in a SQL Database. 
Walking and bicycling are the main modes of transportation for navigation which differs Kalamazoo Route Planner from other Navigation Applications. 

Given a set of points, the best route is then calculated and drawn on a map of the Kalamazoo area. 
The algorithm considers some stress factors when doing the calculations. Among them are speed limits, the typology of a road or path, as well as the amount of activity on them. 
In addition, the website will provide information about nearby amenities like pharmacies, bike parking, grocery stores, and more. 

***

### Setup:
1. download the repository from GitHub
2. open the terminal and navigate to the repository
3. install the requirements by running `python3 install.py`
4. create the database by running `python3 create_db.py` ([DB_create.py](src%2FDB_Management%2FDB_create.py))
5. This will create the database and populate it with the data from OSM, Modeshift and Imagine Kalamazoo 2025.
6. Run the server by running `python3 main.py` ([main.py](src%2Fmain.py))
7. Open a browser and navigate to `localhost:5000`
8. The website should now be running
9. If you want to have the website accessible from other devices on your network, you can access it by using the IP address of the computer running the server instead of `localhost`
10. If you want to use the website online you can use the port forwarding feature of your router to make the website accessible from the internet.


***

### Usage:

manual here






