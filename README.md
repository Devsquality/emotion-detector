# Enhanced Emotion Detector

A web application that analyzes emotions in text using IBM Watson Natural Language Understanding API. The application detects both base emotions and derived emotional states.

## Features

- Detects base emotions (joy, sadness, fear, disgust, anger)
- Calculates derived emotions (excitement, anxiety, frustration, contentment)
- Interactive web interface with color-coded emotion bars
- Real-time analysis
- Error handling
- Responsive design

## Project Structure

```
emotion-detector/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend interface
├── test_app.py           # Unit tests
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── .env.example          # Example environment variables
├── sample_texts.txt      # Sample texts for testing
└── README.md            # This file
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your IBM Watson credentials:
     - WATSON_API_KEY
     - WATSON_URL

3. Run the application:
   ```bash
   python app.py
   ```

4. Run tests:
   ```bash
   pytest test_app.py
   ```

## Usage

1. Open http://127.0.0.1:5000 in your browser
2. Enter text in the input field
3. Click "Analyze Emotions"
4. View the emotion analysis results:
   - Base emotions from Watson NLU
   - Derived emotional states
   
Sample texts for testing can be found in `sample_texts.txt`

## Technologies Used

- Python 3.x
- Flask
- IBM Watson NLU
- HTML/CSS/JavaScript
- pytest for testing
