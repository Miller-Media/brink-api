from brink import app

# Register all api endpoints
import brink.api as api
for version in api.versions:
	for module in api.endpoints( version ):
		if hasattr( module, 'blueprint' ):
			app.register_blueprint( module.blueprint, url_prefix="/" + str( version ) )

# Startup server
if __name__ == '__main__':
	app.run( host=app.config[ 'HOST' ], port=app.config[ 'PORT' ] )