
class ApiException( Exception ):
	""" An exception class for our api """
	
	# error message
	_error = None 
	
	def __init__( self, error=None ):
		if error is not None:
			if isinstance( error, str ):
				self._error = { 'error': error }, 400
			else:
				self._error = error
		else:
			self._error = { 'error' : 'Unspecified error.' }, 400

