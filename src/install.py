# pip install all the packages needed for the website to run
import os
import sys
import subprocess


def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])
	print('Installed ' + package + ' successfully! \n\n\n')


install("numpy")
install("flask")
install("python-dotenv")
install("pandas")
install("OSMPythonTools")
install("pykml")
install("geopy")
install("geopandas")
install("folium")
install("gpxpy")
