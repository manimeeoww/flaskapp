from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust this for your specific domain

# Load the model
model = tf.keras.models.load_model('mymodel.h5')

# Define flower categories and detailed info
categories = {
    'Chamomile': {
        'scientific_name': 'Matricaria chamomilla (German chamomile) or Chamaemelum spp. (Roman chamomile)',
        'origin': 'Native to Europe, western Asia, and northern Africa',
        'family': 'Asteraceae (Compositae)',
        'symbolism': 'Known for its soothing properties, it symbolizes relaxation, peace, and healing.',
        'link':  'https://en.wikipedia.org/wiki/Chrysanthemum',
        'image': 'https://i.pinimg.com/564x/26/d8/e8/26d8e8760154d8229ef3ae6b3a078f6b.jpg'
    },
    'Chrysanthemum': {
        'scientific_name': 'Chrysanthemum spp. (Various species)',
        'origin': 'Native to Asia and northeastern Europe',
        'family': 'Asteraceae (Compositae)',
        'symbolism': 'Symbolizes longevity, loyalty, joy, and optimism.',
        'link':  'https://en.wikipedia.org/wiki/Chrysanthemum',
        'image': 'https://i.pinimg.com/564x/20/63/25/206325bae5f105956f255845eb42bbcc.jpg'
    },
    # Add more flower details as needed
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Process the image
        img = Image.open(file.stream).resize((224, 224))  # Adjust to your model's input size
        img_array = np.array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Map prediction to flower category
        flower_name = list(categories.keys())[predicted_class]
        flower_info = categories.get(flower_name, {})

        # Return prediction and flower details
        return jsonify({
            'prediction': flower_name,
            'scientific_name': flower_info['scientific_name'],
            'origin': flower_info['origin'],
            'family': flower_info['family'],
            'symbolism': flower_info['symbolism'],
            'link': flower_info['link'],
            'image': flower_info['image']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
