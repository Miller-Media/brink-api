from brink import app, db
import brink.api as api

# This will create the database using SQLAlchemy
import brink.models
db.create_all()

# Register all api endpoints
for version in api.versions:
	for module in api.endpoints( version ):
		if hasattr( module, 'blueprint' ):
			app.register_blueprint( module.blueprint, url_prefix="/api/" + str( version ) )


# Startup server
if __name__ == '__main__':
	app.run( host=app.config[ 'HOST' ], port=app.config[ 'PORT' ] )