from brink import db
from base import BaseModel, BaseModelWithMeta
from sqlalchemy.ext.associationproxy import association_proxy

class User( BaseModelWithMeta ):
    """ A user of the system """
    
    __tablename__ = 'users'
    
    username            = db.Column( 'username', db.String( 200 ), nullable=False, unique=True )
    email               = db.Column( 'email', db.String( 255 ), nullable=False, unique=True )
    password            = db.Column( 'password', db.String( 160 ), nullable=False )
    first_name          = db.Column( 'first_name', db.String( 255 ), nullable=True )
    last_name           = db.Column( 'last_name', db.String( 255 ), nullable=True )
    created             = db.Column( 'date_created', db.DateTime, default=db.func.current_timestamp() )
    modified            = db.Column( 'date_modified', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp() )

    meta                = db.relationship( 'UserMeta', cascade="all, delete-orphan", lazy='dynamic' )

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

    def setPassword( self, password ):
        """ Set the password for a user
        
        Args:
            password (str): 				The plain text password for the user
            
        Returns:
            None
            
        Raises:
            PasswordException:				An exception if the password is not acceptable
        """
        
        from brink.exceptions import PasswordException
        from werkzeug.security import generate_password_hash
        
        # error if password is empty
        if password is None or password == '':
            raise PasswordException( 'Password cannot be empty!' )
        
        self.password = generate_password_hash( password )


class UserMeta( BaseModel ):
    """ Metadata attached to a user in the system """
    
    __tablename__ = 'users_meta'
    
    id       = None
    key      = db.Column( 'meta_key', db.String( 255 ), nullable=False, primary_key=True )
    value    = db.Column( 'meta_value', db.String( 255 ), nullable=True )
    user_id  = db.Column( 'user_id', db.Integer, db.ForeignKey( 'users.id' ), primary_key=True )
    created  = db.Column( 'date_created', db.DateTime, default=db.func.current_timestamp() )
    
    user     = db.relationship( 'User' )
    
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
        

class ApiUser( BaseModel ):
    """ An api user """
    
    __tablename__ = 'api_users'
    
    username = db.Column( 'username', db.String( 200 ), nullable=False, unique=True )
    password = db.Column( 'password', db.String( 200 ), nullable=False )
       
    authTokens          = db.relationship( 'AuthToken', cascade="all, delete-orphan", lazy='dynamic' )
    
    def setPassword( self, password ):
        """ Set the password for a user
        
        Args:
            password (str): 				The plain text password for the user
            
        Returns:
            None
            
        Raises:
            PasswordException:				An exception if the password is not acceptable
        """
        
        from brink.exceptions import PasswordException
        from werkzeug.security import generate_password_hash
        
        # error if password is empty
        if password is None or password == '':
            raise PasswordException( 'Password cannot be empty!' )
        
        self.password = generate_password_hash( password )