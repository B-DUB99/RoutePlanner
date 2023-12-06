# Importing the modules
import sys
import os
from flask import Flask
from scripts.views import views
from scripts.test import Test
from dotenv import load_dotenv
from time import sleep


# Loading the environment variables
def get_env():
	# check if .env file exists and load it, otherwise use default values
	if os.path.exists(".env"):
		load_dotenv()
		host_ip = os.getenv("HOST_IP")
		host_port = os.getenv("HOST_PORT")
		debug = False
	else:
		print("No .env file found. Using default values.")
		host_ip = 'localhost'
		host_port = 8080
		debug = True
	print(f"Host IP: {host_ip}\nHost Port: {host_port}\n")
	return host_ip, host_port, debug


# Running the website
def run_website():
	host_ip, host_port, debug_TF = get_env()
	app = Flask(__name__, static_folder="static/", template_folder="templates/")
	app.secret_key = "testing"
	app.register_blueprint(views, url_prefix="/")
	app.run(host=host_ip, port=host_port, debug=debug_TF)


if __name__ == '__main__':
	# sys.argv = [arg.lower() for arg in sys.argv]
	sys.argv = ['.\\main.py', '-t']  # for testing DELETE THIS LINE

	if len(sys.argv) == 1:
		sleep(1)  # delay for network route to be established
		run_website()

	if '-t' in sys.argv or '-test' in sys.argv:
		pass
		Test()
	else:
		error = "Invalid argument(s)."
		print(error)
