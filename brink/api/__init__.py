import importlib, os, pkgutil

from werkzeug.security import check_password_hash
from brink.api.decorators import require_auth, handle_errors, error
from brink.api.utils import get_params
from brink.models import User
from brink import app
import flask_jwt

# get a list of the subfolders in the api directory
versions = next( os.walk( os.path.dirname( os.path.realpath( __file__ ) ) ) )[1]

def endpoints( version ):
	""" Return a list of endpoint submodules for a particular api version
	
	This function will iterate the modules in the particular api version folder, import them,
	and then return them as a list
	
	Args:
		version (str): 		The version subfolder to load modules from
		
	Returns
		list:				List of endpoint modules
		
	"""
	package = importlib.import_module( 'brink.api.' + version )
	pkgpath = os.path.dirname( package.__file__ )
	modules = [ name for _, name, _ in pkgutil.iter_modules( [pkgpath] ) ]
	return [ importlib.import_module( 'brink.api.' + version + '.' + module ) for module in modules ]
	
def jwt_authenticate( username, password ):
    """ Handle authorizing a username/password for api access
    
    """

    # find user with provided username and password
    user = User.query.filter(User.username == username).first()

    if user is None:
        raise ApiException('Authentication failed.')

    # check for correct password
    if not check_password_hash(user.password, password):
        raise ApiException('Authentication failed.')

    return user
  
def jwt_identity( payload ):
    """ Load an identity from the jwt payload
    
    """
   
    return payload
   
jwt = flask_jwt.JWT(app, jwt_authenticate, jwt_identity)

def getUser():

    return User.load( flask_jwt.current_identity.get( 'identity', None ) )