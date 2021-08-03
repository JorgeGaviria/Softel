from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'mykey',
        DATABASE_HOST = 'localhost',
        DATABASE_USER = 'jorgexampp',
        DATABASE_PASSWORD= 'conectarse102938',
        DATABASE = 'softel'
    )
    from . import db
    db.init_app(app)
    
    from . import admin
    app.register_blueprint(admin.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import empleado
    app.register_blueprint(empleado.bp)

    from . import public
    app.register_blueprint(public.bp)
    
    from . import cliente
    app.register_blueprint(cliente.bp)

    from . import reserva
    app.register_blueprint(reserva.bp)

    from . import habitacion
    app.register_blueprint(habitacion.bp)

    


    
    
    return app