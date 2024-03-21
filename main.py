from flask_cors import CORS
from flask import Flask, jsonify, request

from src import db


client = db.ClientWrapper()
app = Flask(__name__)
CORS(app)


@app.route('/search', methods=['POST'])
def search():
    raw_query = request.json.get('query')
    results = client.search(raw_query)
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
