# Import Libraries
from flask import jsonify, Blueprint
from flask_cors import CORS
ptt_blueprints = Blueprint('owner', __name__)
CORS(ptt_blueprints)

@ptt_blueprints.route('/')
def api():
    # return in JSON format. (For API)
    return jsonify({"message": "Ptt Ok"})
