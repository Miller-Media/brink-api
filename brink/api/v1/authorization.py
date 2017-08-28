from flask import Blueprint
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from brink.models import User
from brink.exceptions import PasswordException
from brink.api.exceptions import ApiException
import brink.api as api
import uuid

# the blueprint that will be imported
blueprint = Blueprint('authorization', __name__)


@blueprint.route('/login', methods=['POST'])
@api.handle_errors()
def login():
    """ Login to application

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    from flask_jwt import _jwt
    
    # get request parameters
    params = api.get_params(require=['username', 'password'])

    # check if username exists
    username_exists = User.query.filter(User.username == params['username']).count() > 0
    if not username_exists:
        raise ApiException('Username does not exist.')

    # find user with provided username and password
    user = User.query.filter(User.username == params['username']).first()

    if user is None:
        raise ApiException('User not found.')

    # check for correct password
    if not check_password_hash(user.password, params['password']):
        raise ApiException('Incorrect password.')

    user_data = user.asApiDict()
    user_data['sessions'] = [ session.id for session in user.sessions ]
    user_data['jwt_token'] = api.jwt.jwt_encode_callback( user )

    # remap keys for expected response
    params_to_attributes = {
        'date_created': 'created',
        'date_modified': 'modified'
    }
    
    for new, old in params_to_attributes.iteritems():
        user_data[new] = user_data.pop(old)

    return user_data

