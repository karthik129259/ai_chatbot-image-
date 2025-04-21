from flask import Flask, render_template, request, jsonify
import os
from core.image_api import detect_objects
from core.chatbot import generate_response
from utils.helper import allowed_file

app = Flask(__name__)

# Folder to store uploaded images
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling image upload and processing
@app.route('/process_image', methods=['POST'])
def process_image():
    image_source = None
    question = request.form.get('question', '')
    
    if not question:
        return jsonify({'error': '❌ Please ask a question about the image.'})
    
    # Check if a file was uploaded
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '' and allowed_file(file.filename):
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            image_source = file_path
        elif file.filename != '' and not allowed_file(file.filename):
            return jsonify({'error': '❌ Invalid file format. Please upload an image (.jpg, .jpeg, .png).'})
    
    # If no file uploaded, check for URL
    if not image_source:
        image_url = request.form.get('image_url', '')
        if image_url:
            image_source = image_url
    
    # Validate that we have an image source
    if not image_source:
        return jsonify({'error': '❌ Please upload an image or provide a valid image URL.'})

    # Call the API for object detection
    detected_objects = detect_objects(image_source)
    
    if not detected_objects:
        return jsonify({'error': '❌ Failed to detect objects in the image.'})

    # Generate the response based on detected objects and question
    response = generate_response(detected_objects, question)
    
    return jsonify({
        'response': response,
        'detected_objects': detected_objects  # Optionally return detected objects
    })

if __name__ == '__main__':
    app.run(debug=True)