from flask_cors import CORS
from flask import Flask, jsonify, request

from src import db


client = db.ClientWrapper()
app = Flask(__name__)
CORS(app)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/ping', methods=['GET'])
def ping():
    result, message = client.ping()
    return jsonify({'ping': result, 'message': message})


@app.route('/search', methods=['POST'])
def search():
    raw_query = request.json.get('query')
    results = client.search(raw_query)
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
