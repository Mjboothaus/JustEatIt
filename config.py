import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True  -- turned off - now in the app.run() call if running locally

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious dona'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID     = 'b4f167ed'
SECRET_KEY = '7d441f27d441f27567d441f2b6176a'

# Default option values (for Yummly connections)

TIMEOUT = 15.0
RETRIES = 2

