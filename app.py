from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {'opus'}
API_URL = 'http://10.100.102.6:7823/voice/inference'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze-voice', methods=['POST'])
def analyze_voice():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request ❗'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected ❗'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only .opus allowed ❗'}), 400

    try:
        files = {'file': (file.filename, file.stream, 'audio/opus')}
        response = requests.post(API_URL, files=files)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API call failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
