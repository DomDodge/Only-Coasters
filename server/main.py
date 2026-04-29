from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from database import DB

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


# --- Additional query endpoints ---

@app.route('/queries/operating', methods=['GET'])
def queries_operating():
    try:
        return jsonify(db.get_all_operating_coasters())
    except Exception:
        return jsonify({'error': 'failed to fetch operating coasters'}), 500

@app.route('/queries/defunct', methods=['GET'])
def queries_defunct():
    try:
        return jsonify(db.get_all_defunct_coasters())
    except Exception:
        return jsonify({'error': 'failed to fetch defunct coasters'}), 500

@app.route('/queries/sbno', methods=['GET'])
def queries_sbno():
    try:
        return jsonify(db.get_all_SBNO_coasters())
    except Exception:
        return jsonify({'error': 'failed to fetch SBNO coasters'}), 500

@app.route('/queries/manufacturers/avg_height', methods=['GET'])
def queries_manufacturers_avg_height():
    try:
        return jsonify(db.get_manufacturers_ranked_by_avg_height())
    except Exception:
        return jsonify({'error': 'failed to fetch manufacturers avg height'}), 500

@app.route('/queries/manufacturers/avg_speed', methods=['GET'])
def queries_manufacturers_avg_speed():
    try:
        return jsonify(db.get_manufacturers_ranked_by_avg_speed())
    except Exception:
        return jsonify({'error': 'failed to fetch manufacturers avg speed'}), 500

@app.route('/queries/parks/low_wait_high_attendance', methods=['GET'])
def queries_parks_low_wait_high_attendance():
    try:
        return jsonify(db.get_parks_with_low_wait_high_attendence())
    except Exception:
        return jsonify({'error': 'failed to fetch parks metrics'}), 500


def _parse_percent_param():
    x = request.args.get('x', default=None)
    try:
        if x is None:
            return None, ('missing x param', 400)
        x = float(x)
        if x <= 0 or x > 1:
            return None, ('x must be a decimal between 0 and 1 (exclusive)', 400)
        return x, None
    except ValueError:
        return None, ('x must be a decimal (e.g. 0.05)', 400)


@app.route('/queries/top/age', methods=['GET'])
def queries_top_age():
    x, err = _parse_percent_param()
    if err:
        return jsonify({'error': err[0]}), err[1]
    try:
        return jsonify(db.get_top_x_percent_of_coasters_by_age(x))
    except Exception:
        return jsonify({'error': 'failed to fetch top age coasters'}), 500


@app.route('/queries/top/height', methods=['GET'])
def queries_top_height():
    x, err = _parse_percent_param()
    if err:
        return jsonify({'error': err[0]}), err[1]
    try:
        return jsonify(db.get_top_x_percent_of_coasters_by_height(x))
    except Exception:
        return jsonify({'error': 'failed to fetch top height coasters'}), 500


@app.route('/queries/top/speed', methods=['GET'])
def queries_top_speed():
    x, err = _parse_percent_param()
    if err:
        return jsonify({'error': err[0]}), err[1]
    try:
        return jsonify(db.get_top_x_percent_of_coasters_by_speed(x))
    except Exception:
        return jsonify({'error': 'failed to fetch top speed coasters'}), 500


@app.route('/queries/top/length', methods=['GET'])
def queries_top_length():
    x, err = _parse_percent_param()
    if err:
        return jsonify({'error': err[0]}), err[1]
    try:
        return jsonify(db.get_top_x_percent_of_coasters_by_length(x))
    except Exception:
        return jsonify({'error': 'failed to fetch top length coasters'}), 500

if __name__ == '__main__':
    app.run(debug=True)