import requests
from flask_cors import CORS
from flask import Flask, jsonify, request

from src import scrap, db


client = db.ClientWrapper()
app = Flask(__name__)
CORS(app)


@app.route('/marches-publics', methods=['GET'])
def get_marches_publics():
    try:
        html_content = requests.get(
            'https://www.marches-publics.gouv.fr/?page=Entreprise.EntrepriseAdvancedSearch&AllCons'
        ).text
    except Exception as e:
        return jsonify({'error': 'request failed', 'message': str(e)})

    results = scrap.extract_results(html_content)

    return jsonify({'results': list(results)})


@app.route('/search', methods=['POST'])
def search():
    raw_query = request.json.get('query')
    results = client.search(raw_query)
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
