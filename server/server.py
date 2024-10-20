from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'server'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "This is actually so freaking cool lmao",
        'people': ["yang", "name", "another name"]
    })

@app.route("/api/process_frame", methods=['POST'])
def process_frame():
    try:
        if 'image' not in request.files:
            app.logger.error('No file part in the request')
            return 'No file part', 400
        file = request.files['image']
        if file.filename == '':
            app.logger.error('No selected file')
            return 'No selected file', 400
        file_path = os.path.join(UPLOAD_FOLDER, 'capture.png')
        file.save(file_path)
        app.logger.info(f'File successfully saved to {file_path}')
        return jsonify({'message': 'File successfully uploaded'}), 200
    except Exception as e:
        app.logger.error(f'Error processing file: {e}')
        return jsonify({'message': 'Error processing file'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)