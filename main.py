import os
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import timedelta
from dotenv import load_dotenv

from src import db, llm, utils


load_dotenv()

client = db.ClientWrapper()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

CORS(app)
jwt = JWTManager(app)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/ping', methods=['GET'])
def ping():
    result, message = client.ping()
    return jsonify({'ping': result, 'message': message})


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username != os.getenv('LOGIN_USER') or password != os.getenv('LOGIN_PASS'):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(token=access_token)


@app.route('/search', methods=['POST'])
@jwt_required()
def search():
    raw_query = request.json.get('query', '')
    search_method = request.json.get('method', 'vector')

    if raw_query == '':
        search_method = utils.SearchParameters.text_method

    if search_method == utils.SearchParameters.vector_method:
        raw_query, exception = llm.LLM().get_embeddings(raw_query)
        if exception != '':
            return jsonify({'results': [], 'message': 'Failed to get embeddings.'})
    results = client.search(raw_query, search_method)

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
