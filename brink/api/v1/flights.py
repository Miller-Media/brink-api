from flask import Blueprint
from brink.models import Flight, FlightMeta, FlightDataPoint
from brink.api.exceptions import ApiException
import brink.api as api


# the blueprint that will be imported
blueprint = Blueprint('flights', __name__)

@blueprint.route('/flights', methods=['PUT'])
@api.handle_errors()
@api.require_auth()
def create_flight():
    """ Create a new flight

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 201)
        dict:		Api response headers (optional) (default: {})
    """

    user = api.getUser()
    
    if user.id != 1:
        raise ApiException( 'Not authorized.' )

    # get request parameters
    params = api.get_params()

    data = Flight().filterParams(params, exclude=['id', 'created'])

    # create the flight
    flight = Flight(**data)
    flight.save()
    
    return {
               'success': 'Flight created.'
           }, 201

@blueprint.route('/flights/<int:flight_id>', methods=['GET'])
@api.handle_errors()
@api.require_auth()
def get_flight(flight_id):
    """ Get flight data

    Args:
        flight_id (int): 			The flight id

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    # error if flight not found
    flight = Flight.load(flight_id)
    if flight is None:
        raise ApiException('Flight not found.')

    return flight.asApiDict()

@blueprint.route('/flights/<int:flight_id>', methods=['DELETE'])
@api.handle_errors()
@api.require_auth()
def delete_flight(flight_id):
    """ Delete a flight

    Args:
        flight_id (int): 			The flight id

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    user = api.getUser()
    
    # make sure user is authorized
    if user.id == 1:

        # load the flight
        flight = Flight.load(flight_id)

        # error if flight doesn't exist
        if flight is None:
            raise ApiException('flight could not be found.')

        # delete the flight
        flight.delete()

        return {
                   'success': 'flight deleted.'
               }, 200

    # flight has not been deleted
    raise ApiException('Not authorized.')

@blueprint.route('/flights/<int:flight_id>/data', methods=['PUT'])
@api.handle_errors()
@api.require_auth()
def create_flight_data():
    """ Create a new flight data point

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 201)
        dict:		Api response headers (optional) (default: {})
    """

    user = api.getUser()
    
    if user.id != 1:
        raise ApiException( 'Not authorized.' )

    # error if flight not found
    flight = Flight.load(flight_id)
    if flight is None:
        raise ApiException('Flight not found.')
        
    # get request parameters
    params = api.get_params()

    data = FlightDataPoint().filterParams(params)

    # create the flight
    datapoint = FlightDataPoint(**data)
    datapoint.flight = flight.id
    datapoint.save()
    
    return {
               'success': 'Flight data point created.'
           }, 201

@blueprint.route( '/flights/<int:flight_id>/data', methods=[ 'POST' ] )
@api.handle_errors()
@api.require_auth()
def get_flight_data_paged( session_id ):
    """ Get the messages for a session in paged format

    Args:
        session_id (int): 			The session id

    Returns:
        dict:		Api response
        int:		Api response code (optional) (default: 200)
        dict:		Api response headers (optional) (default: {})
    """

    params = api.get_params()    
    
    page = params['page'] if 'page' in params else 1
    per_page = params['per_page'] if 'per_page' in params else 20
    
    # error if flight not found
    flight = Flight.load( flight_id )
    if flight is None:
        raise ApiException( 'Flight not found.' )

    paged_data = flight.data.paginate( page=page, per_page=per_page, error_out=False )
    
    return {
        'pages'    : paged_data.pages,
        'total'    : paged_data.total,
        'page'     : paged_data.page,
        'per_page' : paged_data.per_page,
        'messages' : { message.id: message.asApiDict() for message in paged_messages.items }
    }  

@blueprint.route( '/flights/<int:flight_id>/meta', methods=[ 'GET' ] )
@api.handle_errors()
@api.require_auth()
def get_flight_meta_keys( flight_id ):
    """ Get the meta data keys for a flight

    Args:
        flight_id (int):            The flight id

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """
    
    # load the flight
    flight = Flight.load( flight_id )

    # error if flight doesn't exist
    if flight is None:
        raise ApiException( 'Flight could not be found.' )
        
    return { 'keys': [ meta.key for meta in flight.meta ] }

@blueprint.route( '/flights/<int:flight_id>/meta', methods=[ 'POST' ] )
@api.handle_errors()
@api.require_auth()
def get_flight_meta( flight_id ):
    """ Get the meta data for the flight

    Args:
        flight_id (int):            The flight id

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """
    
    # get the request params
    params = api.get_params( require=[ 'keys' ] )
    
    if not isinstance( params['keys'], list ):
        raise ApiException( 'keys must be provided as an array' )
    
    # load the flight
    flight = Flight.load( flight_id )

    # error if flight doesn't exist
    if flight is None:
        raise ApiException( 'Flight could not be found.' )
        
    return { meta.key: flight.getMeta(meta.key) for meta in flight.meta if meta.key in params['keys'] }

@blueprint.route( '/flights/<int:flight_id>/meta', methods=[ 'PUT' ] )
@api.handle_errors()
@api.require_auth()
def set_flight_meta_values( flight_id ):
    """ Update the meta data for the flight

    Args:
        flight_id (int):            The flight id

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """
    
    params = api.get_params()

    # load the flight
    flight = Flight.load( flight_id )

    # error if flight doesn't exist
    if flight is None:
        raise ApiException( 'flight could not be found.' )
   
    for key, value in params.iteritems():
        flight.setMeta( key, value )
        
    flight.save()
    
    return { 'success': 'Flight meta updated.' }

@blueprint.route( '/flights/<int:flight_id>/meta/<string:meta_key>', methods=[ 'DELETE' ] )
@api.handle_errors()
@api.require_auth()
def delete_flight_meta_key( flight_id, meta_key ):
    """ Delete flight meta

    Args:
        flight_id (int):            The flight id
        meta_key (str):            The meta key to delete

    Returns:
        dict:       Api response
        int:        Api response code (optional) (default: 200)
        dict:       Api response headers (optional) (default: {})
    """

    # load the flight
    flight = Flight.load( flight_id )

    # error if flight doesn't exist
    if flight is None:
        raise ApiException( 'flight could not be found.' )

    flight.deleteMeta( meta_key )
    
    return { 'success': 'Flight meta deleted.' }
    