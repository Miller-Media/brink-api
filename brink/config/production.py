# Statement for enabling the development environment
DEBUG = False

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Facebook Graph API credentials
FACEBOOK_APP_ID = "1176466902366484"
FACEBOOK_APP_SECRET = "86767be2734678ee96c89aeb63eebb0a"
