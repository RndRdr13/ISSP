from flask import Flask, request, jsonify
from flask_cors import CORS
from snap_website_analyzer_final import analyze_website

app = Flask(__name__)
CORS(app)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400
    result = analyze_website(url)
    return jsonify(result)

if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0", port=5000)

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
