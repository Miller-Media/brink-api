from brink import db
from base import BaseModel, BaseModelWithMeta
from sqlalchemy.ext.associationproxy import association_proxy

class Flight( BaseModelWithMeta ):
    """ A brink flight """
    
    __tablename__ = 'flights'
    
    created             = db.Column( 'date_created', db.DateTime, default=db.func.current_timestamp() )

    meta                = db.relationship( 'FlightMeta', cascade="all, delete-orphan", lazy='dynamic' )
    data_points         = db.relationship( 'FlightDataPoint', cascade="all, delete-orphan", lazy='dynamic' )

    def __init__( self, *args, **kwargs ):
        """ Constructor
        
        This constructor allows us to pass in select object properties without naming them
        for ease of use. They must be in the prescribed order if we do. Named arguments
        are simply passed on to the base class for assignment as usual.
        
        Args:
            #1:		username
            #2:		email
            #3:		password
            #4:		first_name
            #5:		last_name
            
        Returns:
            None
        """
        
        if len( args ) > 0 : self.username     = args[0]
        if len( args ) > 1 : self.email        = args[1]
        if len( args ) > 2 : self.password     = args[2]
        if len( args ) > 3 : self.first_name   = args[3]
        if len( args ) > 4 : self.last_name    = args[4]
        if len( kwargs ) > 0 : super( User, self ).__init__( **kwargs )


class FlightMeta( BaseModel ):
    """ Metadata attached to a flight in the system """
    
    __tablename__ = 'flights_meta'
    
    id         = None
    key        = db.Column( 'meta_key', db.String( 255 ), nullable=False, primary_key=True )
    value      = db.Column( 'meta_value', db.String( 255 ), nullable=True )
    flight_id  = db.Column( 'flight_id', db.Integer, db.ForeignKey( 'flights.id' ), primary_key=True )
    created    = db.Column( 'date_created', db.DateTime, default=db.func.current_timestamp() )
    
    flight     = db.relationship( 'Flight' )
    
    def __init__( self, *args, **kwargs ):
        """ Constructor
        
        This constructor allows us to pass in select object properties without naming them
        for ease of use. They must be in the prescribed order if we do. Named arguments
        are simply passed on to the base class for assignment as usual.
        
        Args:
            #1:		The meta key
            #2:		The meta value
            
        Returns:
            None
        """
        
        if len( args ) > 0 : self.key = args[0]
        if len( args ) > 1 : self.value = args[1]
        if len( kwargs ) > 0 : super( UserMeta, self ).__init__( **kwargs )
        
class FlightDataPoint( BaseModel ):
    """ Recorded data for a given flight """
    
    __tablename__ = 'flights_data'
    
    flight_id   = db.Column( 'flight_id', db.Integer, db.ForeignKey( 'flights.id' ) )
    timestamp   = db.Column( 'timestamp', db.Integer, nullable=False, default=db.func.current_timestamp(), index=True )
    coordinateX = db.Column( 'coordinate_x', db.Float, nullable=False )
    coordinateY = db.Column( 'coordinate_y', db.Float, nullable=False )
    pressure    = db.Column( 'pressure', db.Integer, nullable=False )
    temperature = db.Column( 'temperature', db.Integer, nullable=False )
    altitude    = db.Column( 'altitude', db.Integer, nullable=False )
    
    flight     = db.relationship( 'Flight' )
    