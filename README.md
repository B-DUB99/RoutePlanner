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
7. Open a browser and navigate to `localhost:8080`
8. The website should now be running
9. If you want to have the website accessible from other devices on your network, you can access it by using the IP address of the computer running the server instead of `localhost`
10. If you want to use the website online you can use the port forwarding feature of your router to make the website accessible from the internet.


***

### Usage:

#### Markers 

#### Start Marker
![Start_Marker.jpg](files_for_markdown%2FReadme%2FStart_Marker.jpg)

#### End Marker
![End_Marker.jpg](files_for_markdown%2FReadme%2FEnd_Marker.jpg)

by Clicking on the map, you can set a marker. The first marker you set will be the start marker, the second marker will be the end marker.
By pushing the marker to a new location, the route will be recalculated.
<br><br><br>

#### Transport 
![transport_tab.jpg](files_for_markdown%2FReadme%2Ftransport_tab.jpg)

Here you can select the mode of transportation. Currently, there are two options, walking and biking.
<br><br><br>

#### Risk Tolerance 
![Risk_Tolerance.jpg](files_for_markdown%2FReadme%2FRisk_Tolerance.jpg)

Here you can select the risk tolerance. The risk tolerance is a value between 0 and 1. The higher the value, the more risk you are willing to take.
The risk tolerance is used to calculate the route. The algorithm will try to avoid roads with a high-risk value.
A Risk level of 1 means that the algorithm will try to avoid all roads with a risk value higher than 1.
Therefore the result of this route will be the safest route possible.

If no Route is found for the User Risk Tolerance, the Risk Tolerance will be increased by 1 and the algorithm will try again until a route is found.
<br><br><br>

#### Amenities 
![Amenities.jpg](files_for_markdown%2FReadme%2FAmenities.jpg)

Here you can select the amenities you want to see on the map. The amenities are divided into multiple categories.
You can select multiple amenities from multiple categories. The amenities will be displayed on the map as markers.
If you click on a marker, you will get more information about the amenity. 
You can also calculate from or to an amenity by clicking on the marker and selecting the Button [Travel Here](#here).
<br><br><br>

#### Export GPX File
![Export_button.jpg](files_for_markdown%2FReadme%2FExport_button.jpg)
 
By exporting the GPX file, you can use the route in other applications like Google Maps or Strada.
<br><br><br>

#### Clear 
![Clear_button.jpg](files_for_markdown%2FReadme%2FClear_button.jpg)

The Clear button will clear the map from all markers and routes. 
<br><br><br>


#### Layer Button 
![layer_button.jpg](files_for_markdown%2FReadme%2Flayer_button.jpg)

The Layer Button (top right corner) will toggle thru the different mao layers like satellite view, bicycle view, etc.
<br><br><br>
