import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from PIL import Image
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": CORS_ORIGIN}})

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
    'French Marigold': {
        'scientific_name': 'Tagetes patula',
        'origin': 'Native to Mexico and Central America',
        'family': 'Asteraceae (Compositae)',
        'symbolism': 'Symbolizes passion and creativity. It\'s also associated with positive energy and good fortune.',
        'link':  'https://en.wikipedia.org/wiki/Tagetes',
        'image': 'https://i.pinimg.com/564x/54/1f/e7/541fe7d7d8a5f3db275336ae7894dc17.jpg'
    },
    'Lavender': {
        'scientific_name': 'Lavandula spp. (Various species)',
        'origin': 'Native to the Mediterranean region, Africa, and India',
        'family': 'Lamiaceae (mint family)',
        'symbolism': 'Represents calmness, serenity, and grace. It\'s often associated with cleanliness and relaxation.',
        'link':  'https://en.wikipedia.org/wiki/Lavender',
        'image': 'https://i.pinimg.com/564x/b8/1d/43/b81d431f9a1ba4859151b510c4adfd72.jpg'
    },
    'Lotus': {
        'scientific_name': 'Nelumbo nucifera',
        'origin': 'Native to Asia and Australia',
        'family': 'Nelumbonaceae',
        'symbolism': 'Represents purity, enlightenment, and rebirth in various cultures, particularly in Asian religions like Buddhism and Hinduism.',
        'link':  'https://en.wikipedia.org/wiki/Nelumbo_nucifera',
        'image': 'https://i.pinimg.com/564x/3e/22/04/3e220427f4b5876085370d5620d99883.jpg'
    },
    'Passion Flower': {
        'scientific_name': 'Passiflora spp. (Various species)',
        'origin': 'Native to tropical and subtropical regions of the Americas',
        'family': 'Passiflorine (passionflower family)',
        'symbolism': 'Represents faith, passion, and spirituality. The intricate structure of its flower is often seen as a symbol of the Passion of Christ.',
        'link':  'https://en.wikipedia.org/wiki/Passiflora',
        'image': 'https://i.pinimg.com/564x/9d/ec/97/9dec97f84dbdb1f6eb7edf79f247abec.jpg'
    },
    'Poppy': {
        'scientific_name': 'Eschscholzia californica',
        'origin': 'Native to California, USA, and adjacent areas of Mexico',
        'family': 'Papaveraceae (poppy family)',
        'symbolism': 'Represents imagination, success, and remembrance. It\'s also associated with relaxation and restful sleep.',
        'link':  'https://en.wikipedia.org/wiki/Eschscholzia_californica',
        'image': 'https://i.pinimg.com/564x/d9/07/a8/d907a83fdf5e5248f32951973065ca6b.jpg'
    },
    'Purple coneflower': {
        'scientific_name': 'Echinacea purpurea',
        'origin': 'Native to eastern and central North America',
        'family': 'Asteraceae (Compositae)',
        'symbolism': 'Known for its medicinal properties and immune-boosting benefits. Represents strength, health, and healing.',
        'link':  'https://en.wikipedia.org/wiki/Echinacea',
        'image': 'https://i.pinimg.com/564x/12/9d/0d/129d0d619d02c62aaa7b1f5dc24ebad6.jpg'
    },
    'Rose': {
        'scientific_name': 'Rosa spp. (Various species)',
        'origin': 'Roses are native to various world regions, depending on the species.',
        'family': 'Rosaceae',
        'symbolism': 'Roses have numerous meanings depending on color and context. Generally, they symbolize love, beauty, and passion.',
        'link': 'https://en.wikipedia.org/wiki/Rose',
        'image': 'https://i.pinimg.com/736x/45/52/73/45527396d88c20076864d2da0a9a84d5.jpg'
    },
    'Sunflower': {
        'scientific_name': 'Helianthus annuus',
        'origin': 'Native to North America',
        'family': 'Asteraceae (Compositae)',
        'symbolism': 'Represents adoration, loyalty, and longevity. The sunflower\'s vibrant yellow color symbolizes vitality and happiness.',
        'link': 'https://en.wikipedia.org/wiki/Common_sunflower',
        'image': 'https://i.pinimg.com/564x/c1/bd/9e/c1bd9eb5b0334800520a78b57d543935.jpg'
    }
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400

        img = Image.open(file.stream).resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        logging.debug(f'Predicted class: {predicted_class}')
        logging.debug(f'Total categories: {len(categories)}')

        if predicted_class >= len(categories):
            return jsonify({'error': 'Predicted class index out of range'}), 500

        flower_name = list(categories.keys())[predicted_class]
        flower_info = categories.get(flower_name, {})

        return jsonify({
            'prediction': flower_name,
            'scientific_name': flower_info.get('scientific_name', 'N/A'),
            'origin': flower_info.get('origin', 'N/A'),
            'family': flower_info.get('family', 'N/A'),
            'symbolism': flower_info.get('symbolism', 'N/A'),
            'link': flower_info.get('link', ''),
            'image': flower_info.get('image', '')
        }), 200

    except Exception as e:
        logging.error(f'Error in prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500
        
# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = CORS_ORIGIN
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

if __name__ == "__main__":
    app.run(debug=True)
