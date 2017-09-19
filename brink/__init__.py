from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

class FlexibleResponse( Response ):
	""" Flexible flask response class
	
	This class is used as a replacement to the standard flask response.
	It allows us to return a dict directly to be sent as json output, or
	an xml string to be sent as xml output.
	
	"""
	def __init__( self, response, *args, **kwargs ):
		""" Constructor 
		
		Args:
			response:	The response content
		
		Kwargs:
			mimetype/contenttype:	The mime-type of the response
			
		Returns:
			None
		"""
		
		# if an explicit content type is not set, attempt to auto-detect it
		if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
			if isinstance( response, str ) and response.startswith( '<?xml' ):
				kwargs[ 'mimetype' ] = 'application/xml'
		
		# let the base class construct the rest of the response
		super( FlexibleResponse, self ).__init__( response, *args, **kwargs )

	@classmethod
	def force_type( self, response, environ=None ):
		""" Convert a non-standard response into one that's acceptable
		
		Args:
			response:	The response that needs to be converted
		
		Returns:
			Response:	A valid flask response
		"""
		
		# auto jsonify dicts
		if isinstance( response, dict ):
			
			# debug responses
			app._debug( "Response: " + str( response ), timestamp=False )
			
			response = jsonify( response )
		
		# let the base class do the rest
		return super( FlexibleResponse, self ).force_type( response, environ )
		
class Brink( Flask ):
	""" Our main app
	
	A subclass of the Flask class that we can customize to our needs.
	
	"""
	
	# set the custom response class for our app
	response_class = FlexibleResponse
	
	# application base path ( the parent directory of this file )
	base_path = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )

	def _debug( self, message, *args, **kwargs ):
		""" Write a debug message out
		
		Args:
			message (str):				The debug message
		"""
		
		# only write debug messages when the app is in debug mode
		if not self.debug: return
		
		# write message to a debug log file
		self.log( message, 'debug', *args, **kwargs )
	
	def log( self, message, file, timestamp=True, separate=False ):
		""" Log a message to a file
		
		Args:
			message (str):					Message to log
			file (str):						File to write the log to
			timestamp (bool):				Whether to include a timestamp with the log
		
		Returns: 
			None
		"""
		
		# add timestamp
		if timestamp:
			from time import gmtime, strftime
			logtime = strftime( "%Y-%m-%d %H:%M:%S", gmtime() )
			message = "> " + logtime + "\n" + str( message )
		
		# add separation
		if separate:
			message = "\n--------------------\n\n" + message		
		
		with open( self.base_path + '/' + file + ".log", "a" ) as log:
			log.write( str( message ) + "\n" )
		
		
### Init App ###
app = Brink( __name__ )
CORS(app)

# Configuration
app.config.from_object( 'config' )
app.url_map.strict_slashes = False

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy( app )
