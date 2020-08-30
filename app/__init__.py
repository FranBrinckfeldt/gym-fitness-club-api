from flask import Flask, jsonify
from .routes import users_blueprint, evaluaciones_blueprint
from .errors import http_errors

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False

@app.route('/')
def hello_world():
    return 'Gym Fitness Club - Flask'

app.register_blueprint(evaluaciones_blueprint, url_prefix = '/evaluaciones')
app.register_blueprint(users_blueprint)

app.register_blueprint(http_errors)