# import itertools
import sqlite3
from collections import deque
from geopy import distance
from pykml import parser
from OSMPythonTools.overpass import Overpass
from OSMPythonTools.overpass import overpassQueryBuilder

def main():
	print("Updating database...")
	# try to connect to the database file if it exists, otherwise create a new one
	try:
		connection = sqlite3.connect('../db/routeplanning.db')
		print("Opened database successfully")
	except:
		print("Error connecting to database")
		return

	# create a cursor object to execute SQL commands
	cursor = connection.cursor()



	# commit and close
	connection.commit()
	connection.close()




if __name__ == "__main__":
	main()
