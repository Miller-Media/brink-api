from flask import Blueprint, request
from brink.models import User, AuthToken, DeviceToken
from brink.api.exceptions import ApiException
from brink.exceptions import PasswordException
import brink.api as api
from brink import app

# the blueprint that will be imported
blueprint = Blueprint('users', __name__)


@blueprint.route('/users', methods=['PUT'])
@api.handle_errors()
def create_user():
    """ Create a new user

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    # get request parameters
    params = api.get_params(require=['email', 'username', 'password'])

    # error if username already exists
    if User.query.filter(User.username == params['username']).count() > 0:
        raise ApiException(api.error('Username already exists.', 409))

    # error if email already exists
    if User.query.filter(User.email == params['email']).count() > 0:
        raise ApiException(api.error('Email already exists.', 409))

    # error if username matches an existing email address
    if User.query.filter(User.email == params['username']).count() > 0:
        raise ApiException(api.error('User with that email address already exists.'))

    data = User().filterParams(params, exclude=['id', 'created', 'modified', 'password'])

    # create the user
    user = User(**data)

    # set the user password
    try:
        user.setPassword(params['password'])

    except PasswordException, e:
        raise ApiException(str(e))

    user.save()

    return {
               'success': 'User created.',
               'response_id': user.id,
               'jwt_token': api.jwt.jwt_encode_callback( user )
           }, 201

@blueprint.route('/users/<int:user_id>', methods=['GET'])
@api.handle_errors()
@api.require_auth()
def get_user(user_id):
    """ Get a user

    Args:
        user_id (int): 		The id of the user being retrieved

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    # get the user
    user = User.load(user_id)
    if user is None:
        raise ApiException(api.error('User not found.'))

    return user.asdict(exclude=['password'])


@blueprint.route('/users/<int:user_id>', methods=['PUT'])
@api.handle_errors()
@api.require_auth()
def update_user(user_id):
    """ Update an existing user

    Args:
        user_id (int): 		The id of the user being updated

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    # get request parameters
    params = api.get_params()

    # get the user
    user = User.load(user_id)
    if user is None:
        raise ApiException(api.error('User not found.'))

    # error if an updated username is already in use
    if 'username' in params and User.query.filter(User.username == params['username'], User.id != user_id).count() > 0:
        raise ApiException(api.error('Username already in use.', 409))

    # update the user attributes
    for prop, val in user.filterParams(params, exclude=['id', 'created', 'modified']).iteritems():
        setattr(user, prop, val)

    user.save()

    return {
        'success': 'User updated.'
    }


@blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@api.handle_errors()
@api.require_auth()
def delete_user(user_id):
    """ Delete an existing user

    Args:
        user_id (int): 		The id of the user being deleted

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    # get request parameters
    params = api.get_params(require=['auth_token'])

    # get the user
    user = User.load(user_id)
    if user is None:
        raise ApiException(api.error('User not found.'))

    if AuthToken.query.filter(AuthToken.value == params['auth_token']).count() > 0:

        # delete the user
        #user.delete()
        
        """ Deleting a user will remove all their linked resources (such as tracks),
        so we should have a hard delete user, and a soft delete user """

        return {
            'success': False,
            'message': 'Not yet implemented.'
        }

    # user has not been deleted
    raise ApiException(api.error('Not authorized.'))

@blueprint.route( '/users/<int:user_id>/meta', methods=[ 'GET' ] )
@api.handle_errors()
@api.require_auth()
def get_user_meta_keys( user_id ):
    """ Get the meta data keys for a user

    Args:
        user_id (int):            The user id

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """
    
    # load the user
    user = User.load( user_id )

    # error if user doesn't exist
    if user is None:
        raise ApiException( 'User could not be found.' )
        
    return { 'keys': [ meta.key for meta in user.meta ] }

@blueprint.route( '/users/<int:user_id>/meta', methods=[ 'POST' ] )
@api.handle_errors()
@api.require_auth()
def get_user_meta( user_id ):
    """ Get the meta data for the user

    Args:
        user_id (int):            The user id

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """
    
    # get the request params
    params = api.get_params( require=[ 'keys' ] )
    
    if not isinstance( params['keys'], list ):
        raise ApiException( 'keys must be provided as an array' )
    
    # load the user
    user = User.load( user_id )

    # error if user doesn't exist
    if user is None:
        raise ApiException( 'User could not be found.' )
        
    return { meta.key: user.getMeta(meta.key) for meta in user.meta if meta.key in params['keys'] }

@blueprint.route( '/users/<int:user_id>/meta', methods=[ 'PUT' ] )
@api.handle_errors()
@api.require_auth()
def set_user_meta_values( user_id ):
    """ Update the meta data for the user

    Args:
        user_id (int):            The user id

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """
    
    params = api.get_params()

    # load the user
    user = User.load( user_id )

    # error if user doesn't exist
    if user is None:
        raise ApiException( 'User could not be found.' )
   
    for key, value in params.iteritems():
        user.setMeta( key, value )
        
    user.save()
    
    return { 'success': 'User meta updated.' }

@blueprint.route( '/users/<int:user_id>/meta/<string:meta_key>', methods=[ 'DELETE' ] )
@api.handle_errors()
@api.require_auth()
def delete_user_meta_key( user_id, meta_key ):
    """ Delete user meta

    Args:
        user_id (int):            The user id
        meta_key (str):            The meta key to delete

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """

    # load the user
    user = User.load( user_id )

    # error if user doesn't exist
    if user is None:
        raise ApiException( 'User could not be found.' )

    user.deleteMeta( meta_key )
    
    return { 'success': 'User meta deleted.' }
