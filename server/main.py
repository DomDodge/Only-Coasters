from flask import Flask, jsonify, abort
from flask_cors import CORS
from .database import DB

app = Flask(__name__, static_folder='../client', static_url_path='')
CORS(app)

db = DB()

@app.route('/')
def index():
    # Serve the client index.html
    return app.send_static_file('index.html')

@app.route('/coasters', methods=['GET'])
def list_coasters():
    try:
        data = db.get_all_coasters()
        # send a small subset for the list to keep payloads light
        summary = [
            { 'rollercoaster_id': c['rollercoaster_id'], 'name': c['name'], 'park_name': c.get('park_name'), 'manufacturer_name': c.get('manufacturer_name') }
            for c in data
        ]
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': 'failed to fetch coasters'}), 500

@app.route('/coasters/<int:coaster_id>', methods=['GET'])
def get_coaster(coaster_id):
    c = db.get_coaster_by_id(coaster_id)
    if not c:
        abort(404)
    return jsonify(c)

if __name__ == '__main__':
    app.run(debug=True)