#! /var/www/ebisu/venv/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/ebisu/venv/lib/python3.6/site-packages')
sys.path.insert(0, '/var/www/ebisu')

from ebisu_flashcards.app import app as application

if __name__ == "__main__":
    application.run(debug=False)
