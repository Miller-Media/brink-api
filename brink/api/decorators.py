from brink.api.exceptions import ApiException
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt import jwt_required, JWTError
from functools import wraps
from flask import request
from brink import app
from brink.models import User
from utils import get_params

def require_auth( *arguments ):
    """ Decorator to automatically require api authorization to access an endpoint 
    
    Args:
        (not implemented):	Possibly a permission requirement to go along with the user authentication
    
    Returns:
        function:	The decorator function
    """
    
    @jwt_required
    def decorator_func( func ):
        @wraps( func )
        def decorated( *args, **kwargs ):
            
            # debug requests
            if app.debug: app._debug( str( request.method ) + " " + str( request.path ) + " " + str( get_params() ), separate=True )
            
            return func( *args, **kwargs )
            
        return decorated
        
    return decorator_func
    
def handle_errors( description='Generic error.', response_code=400 ):
    """ Decorator to automatically return a standard error response for api exceptions
    
    Sets up the default error response that should be sent if and endpoint encounters an
    exception during processing. Will use the specific error response if exception is raised
    using the ApiException class.
    
    Args:
        description (str): 		The default error response message
        response_code (int):	The default error response code
    
    Returns:
        function:	The decorator function
    """
    from brink import app
    
    def decorator_func( func ):
        @wraps( func )
        def decorated( *args, **kwargs ):
        
            try:
                return func( *args, **kwargs )
            
            # return a specific rasied params exception response
            except ApiException, e:					
                return e._error
                
            except JWTError, e:
                return error( str(e), e.status_code )
                
            # return the default error response
            except Exception, e:
            
                # debug exceptions
                if app.debug: 
                    app._debug( "***\nError: " + str( e ) + "\n***\n", timestamp=False )

                return error( description, response_code )
                
        return decorated
        
    return decorator_func

def auth_check( username, password ):
    """ This function is called to check if an auth token is valid and has a permission 
    
    Args:
        username (str):			The username to authorize
        password (str):			The user password
        
    Returns:
        bool:					Returns True if the user is authorized, False otherwise
    """
    from brink.models import ApiUser

    apiUser = ApiUser.query.filter( ApiUser.username == username ).first()
    
    if apiUser is not None:
        return check_password_hash( apiUser.password, password )
        
    return False

def error( description, response_code=400, headers={} ):
    """ Creates an api error response 
    
    Args:
        description (str):		The error message
        response_code (int):	The error response code (optional) (default:400)
        headers (dict):			The response headers (optional) (default={})
    
    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})		
    """
    return { 'error': description }, response_code, headers
