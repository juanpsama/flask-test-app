import sys
import logging

sys.path.insert(0, '/var/www/flask-app/flask-test-app')
sys.path.insert(0, '/var/www/flask-app/venv/lib/python3.10/site-packages/')

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app
from main import app as application