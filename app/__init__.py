from flask import Flask, jsonify
#from .routes import 
from .errors import http_errors

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False

@app.route('/')
def hello_world():
    return 'Gym Fitness Club - Flask'

#app.register_blueprint(products_blueprint, url_prefix = '/products')

app.register_blueprint(http_errors)