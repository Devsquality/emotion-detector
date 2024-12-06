"""
Emotion Detector Package

This package provides emotion analysis functionality using IBM Watson NLU.
It includes both base emotions from Watson and derived emotional states.
"""

from flask import Flask
from dotenv import load_dotenv
import os

# Version information
__version__ = '1.0.0'
__author__ = 'Devsquality'
__email__ = 'Devsquality@gmail.com'

# Load environment variables
load_dotenv()

# Create Flask application instance
app = Flask(__name__)
