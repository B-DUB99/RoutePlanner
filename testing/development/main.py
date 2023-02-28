from flask import Flask
from views import views


def run_website():
    app = Flask(__name__)
    app.secret_key = "testing"
    app.register_blueprint(views, url_prefix="/")
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    run_website()
