# Importing the modules
from flask import Flask
from views import views
import os
from dotenv import load_dotenv


# Loading the environment variables
def get_env():
    # check if .env file exists and load it, otherwise use default values
    if os.path.exists(".env"):
        load_dotenv()
        host_ip = os.getenv("HOST_IP")
        host_port = os.getenv("HOST_PORT")
    else:
        print("No .env file found. Using default values.\n")
        host_ip = 'localhost'
        host_port = 5000
    return host_ip, host_port


# Running the website
def run_website():
    host_ip, host_port = get_env()
    app = Flask(__name__)
    app.secret_key = "testing"
    app.register_blueprint(views, url_prefix="/")
    app.run(debug=True, host=host_ip, port=host_port)


if __name__ == '__main__':
    run_website()
