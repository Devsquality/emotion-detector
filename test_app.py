import pytest
from app import app
import json
import os

@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Emotion Detector' in rv.data

def test_analyze_empty_text(client):
    """Test emotion analysis with empty text"""
    rv = client.post('/analyze',
                    data=json.dumps({'text': ''}),
                    content_type='application/json')
    assert rv.status_code == 400
    assert b'No text provided' in rv.data

@pytest.mark.skipif(not os.getenv('WATSON_API_KEY'), 
                    reason="Watson credentials not available")
def test_analyze_valid_text(client):
    """Test emotion analysis with valid text"""
    test_text = "I am very happy today!"
    rv = client.post('/analyze',
                    data=json.dumps({'text': test_text}),
                    content_type='application/json')
    
    if not os.getenv('WATSON_API_KEY'):
        pytest.skip("Watson credentials not available")
    
    assert rv.status_code == 200
    data = json.loads(rv.data)
    
    # Check base emotions exist
    assert 'joy' in data
    assert 'sadness' in data
    assert 'fear' in data
    assert 'disgust' in data
    assert 'anger' in data
    
    # Check derived emotions exist
    assert 'excitement' in data
    assert 'anxiety' in data
    assert 'frustration' in data
    assert 'contentment' in data

def test_analyze_invalid_json(client):
    """Test emotion analysis with invalid JSON"""
    rv = client.post('/analyze',
                    data='invalid json',
                    content_type='application/json')
    assert rv.status_code == 400

def test_analyze_missing_text_field(client):
    """Test emotion analysis with missing text field"""
    rv = client.post('/analyze',
                    data=json.dumps({'wrong_field': 'some text'}),
                    content_type='application/json')
    assert rv.status_code == 400

@pytest.mark.skipif(not os.getenv('WATSON_API_KEY'), 
                    reason="Watson credentials not available")
def test_emotion_ranges(client):
    """Test that emotion scores are within valid range"""
    test_text = "This is a test text with multiple emotions: happy, sad, angry!"
    rv = client.post('/analyze',
                    data=json.dumps({'text': test_text}),
                    content_type='application/json')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    
    # Check all emotion scores are between 0 and 1
    for emotion, score in data.items():
        assert 0 <= score <= 1, f"Emotion {emotion} score {score} out of range"

@pytest.mark.skipif(not os.getenv('WATSON_API_KEY'), 
                    reason="Watson credentials not available")
def test_long_text(client):
    """Test emotion analysis with long text"""
    long_text = "This is a very long text. " * 100  # Repeat 100 times
    rv = client.post('/analyze',
                    data=json.dumps({'text': long_text}),
                    content_type='application/json')
    assert rv.status_code == 200

@pytest.mark.skipif(not os.getenv('WATSON_API_KEY'), 
                    reason="Watson credentials not available")
def test_special_characters(client):
    """Test emotion analysis with special characters"""
    special_text = "Happy! 😊 #excited @friend $$$"
    rv = client.post('/analyze',
                    data=json.dumps({'text': special_text}),
                    content_type='application/json')
    assert rv.status_code == 200

if __name__ == '__main__':
    pytest.main(['-v'])
