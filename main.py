from flask import Flask
from waitress import serve

server = Flask(__name__, static_url_path="/static")

serve(app, port=8080)
