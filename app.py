from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load the model
diab_model = tf.keras.models.load_model('./model.h5')
shape = (256, 256)

# Create upload directory if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Decode image function
def decode_img(image_path, shape):
    img = load_img(image_path, target_size=shape)
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Mapping labels to categories
LABELS = {0: 'No_Dr', 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Proliferative DR'}

# Default route to render the introduction page
@app.route('/')
def introduction():
    return render_template('introduction.html')

# Prediction page
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            img = decode_img(filepath, shape)
            prediction = diab_model.predict(img)
            predicted_class = np.argmax(prediction, axis=1)[0]
            prediction_text = LABELS[predicted_class]

            # Pass the relative file path to the template
            image_url = f'uploads/{filename}'
            return render_template('index.html', prediction=prediction_text, image_url=image_url)
    
    return render_template('index.html')

# About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Introduction page
@app.route('/introduction')
def introduction_page():
    return render_template('introduction.html')

if __name__ == '__main__':
    app.run(debug=True)
