from brink.api.exceptions import ApiException
from flask import request

def get_params( require=[], ignore=[] ):
	""" Utility method to request parameters from submitted JSON with criteria

	Checks for required fields in the request json content, and excludes
	excluding fields from the return value

	Args:
		require (list): List of key values that the request json must have (optional)
		ignore (list): List of key values that should be removed from return value (optional)

	Returns:
		dict:	The request parameters in a dict

	Raises:
		ParamsException:	An exception will be raised if a required param is missing from the request

	"""
	import brink.api as api
	params = request.get_json()

	if not isinstance( params, dict ):
		params = {}

	# verify required parameters are present
	for param in require:
		if param not in params:
			raise ApiException( "'" + param + "' is a required parameter." )

	# strip params not allowed
	for param in ignore:
		if param in params:
			del params[ param ]

	return params
