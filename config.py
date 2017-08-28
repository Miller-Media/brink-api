# Define the application directory
import os
from datetime import timedelta

BASE_DIR = os.path.abspath( os.path.dirname( __file__ ) )

# Needed here to suppress a warning from sqlalchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# database connection
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join( BASE_DIR, 'app.db' )

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# App host
HOST = 'localhost'

# App port
PORT = 8080

# JWT Authentication Module
JWT_EXPIRATION_DELTA = timedelta( days=365 )