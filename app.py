from flask import Flask, render_template, request, jsonify
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
import os
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Watson NLU
authenticator = IAMAuthenticator(os.getenv('WATSON_API_KEY'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(os.getenv('WATSON_URL'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Basic emotion analysis from Watson
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(emotion=EmotionOptions())
        ).get_result()
        
        base_emotions = response['emotion']['document']['emotion']
        
        # Additional derived emotions based on combinations
        derived_emotions = {}
        
        # Excitement (joy + energy)
        derived_emotions['excitement'] = min(1.0, base_emotions['joy'] * 1.5)
        
        # Anxiety (fear + sadness)
        derived_emotions['anxiety'] = min(1.0, (base_emotions['fear'] + base_emotions['sadness']) / 2)
        
        # Frustration (anger + sadness)
        derived_emotions['frustration'] = min(1.0, (base_emotions['anger'] + base_emotions['sadness']) / 2)
        
        # Contentment (joy - sadness)
        derived_emotions['contentment'] = max(0.0, min(1.0, base_emotions['joy'] - base_emotions['sadness']))
        
        # Combine base and derived emotions
        all_emotions = {**base_emotions, **derived_emotions}
        
        return jsonify(all_emotions)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'error': 'Invalid JSON format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
