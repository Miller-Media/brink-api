from sqlalchemy.orm.properties import ColumnProperty
from dictalchemy import make_class_dictable
from brink import db
import json

class BaseModel( db.Model ):
    """ Base ORM Model
    
    All the brink data models should extend this class to provide a 
    common set of manipulation methods.
    
    """
    
    # This model should not be instantiated directly
    __abstract__  = True
    
    # A standard primary key for persistence to the data store
    id = db.Column( db.Integer, primary_key=True )
    
    @classmethod
    def load( self, id ):
        """ Load a record by id 
        
        A convienient way to fetch a record from the database.
        
        Args:
            id (int):		The id of the record to load
        
        Returns
            Model
        """
        return self.query.get( id )

    def save( self, commit=True ):
        """ Save the record 
        
        Args:
            commit (bool):		Pass False to manually commit the transaction later (default: True)
        
        Returns:
            self
        """
        db.session.add( self )
        if commit: db.session.commit()
        
        return self
        
    def delete( self, commit=True ):
        """ Delete the record 
        
        Args:
            commit (bool):		Pass False to manually commit the transaction later (default: True)
        
        Returns:
            None
        """
        db.session.delete( self )
        if commit: db.session.commit()
        
    def databaseProperties( self ):
        """ List the database column properties of this model
        
        This method is a convenience method to get the properties of this model that are mapped
        directly to a database column.
        
        Args:
            None
            
        Return:
            list
        """
        return [ attribute for attribute, value in self.__mapper__._props.items() if isinstance( value, ColumnProperty ) ]
        
    def filterParams( self, properties, exclude=[] ):
        """ Return a filtered dictionary that contains only keys that map to database properties on this model
        
        Args:
            properties (dict): 			A dictionary containing key/value properties to filter
            exclude (list):				An optional list of additional keys to filter out
            
        Returns:
            dict:						The filtered dictionary with only keys that correspond to properties on this model
        """
        return { 
            property: properties[ property ] 
            for property in self.databaseProperties() 
            if property in properties 
                and property not in exclude 
        }
        
    def asjsondict( self, *args, **kwargs ):
        """ Generate a jsonify(able) dict of this object
        
        Args:
            *args, **kwargs:			Arguments passed through to the asdict() method
        
        Returns:
            dict:						A dict that can be safely jsonified
        """
        from datetime import datetime, date
        
        model_dict = self.asdict( *args, **kwargs )
        
        for key, value in model_dict.iteritems():
        
            # datetime
            if isinstance( value, (datetime, date) ):
                model_dict[ key ] = str( value )
                
        return model_dict

    def asApiDict( self, *args, **kwargs ):
        """ Get a dictionary that represents this object in api responses 
        
        Returns:
            dict
        """
        
        return self.asjsondict( *args, **kwargs )
    
class BaseModelWithMeta( BaseModel ):

    # This model should not be instantiated directly
    __abstract__  = True
    
    def getMeta( self, key ):
        """ Get a meta value
        
        Args:
            key (str):           The meta key to fetch
            
        Returns:
            mixed
        """
        
        meta = self.meta.filter( self.meta._primary_entity.mapper.class_.key == key ).first()
        meta_value = meta.value if meta is not None else None

        if meta_value is not None:
            return json.loads( meta_value )
            
        return None
        
    def setMeta( self, key, value ):
        """ Get a meta value
        
        Args:
            key (str):           The meta key to fetch
            value (mixed):       The value to set, will be automatically json encoded
            
        Returns:
            self
        """
        
        meta = self.meta.filter( self.meta._primary_entity.mapper.class_.key == key ).first()
        
        if meta is not None:
            if value is not None:
                meta.value = json.dumps( value )
                
            else:
                meta.value = None
        
        else:
            meta = self.meta._primary_entity.mapper.class_( key, json.dumps( value ) )
            self.meta.append( meta )
            
        return self
        
    def deleteMeta( self, key ):
        """ Get a meta value
        
        Args:
            key (str):           The meta key to remove
            
        Returns:
            self
        """
        
        meta = self.meta.filter( self.meta._primary_entity.mapper.class_.key == key ).first()
        
        if meta is not None:
            meta.delete()
        
        return self
    
        
# allow our models to easily be converted to dicts
# see: https://pythonhosted.org/dictalchemy/#using-make-class-dictable
make_class_dictable( BaseModel )