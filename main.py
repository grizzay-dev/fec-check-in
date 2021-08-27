from flask import Flask
from waitress import serve
import user as user

app = Flask(__name__, static_url_path="/static")




### ROUTES

@app.route('/')
def root():
    return 'Hello World'

print(user.STATUS)

serve(app, host='0.0.0.0', port=8080)

