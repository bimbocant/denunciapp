import os
from flask import Flask
from . import db
from . import auth

#create and configure the application
def create_app(test_config=None):
    #__name__ -> current Python module. Where the app is located
    #instance_relative_config -> the config files are relative to the instance folder
    #instance folder -> located outside the package. Can hold local data that
    #   shouldn't be commited to version control. Ex: db, config files,others..
    app=Flask(__name__,instance_relative_config=True)

    #sets default config
    #SECRET_KEY -> keep data safe should be random
    #DATABASE -> path to the db file
    #app.instance_path -> oath to the instance folder
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flask-skeleton.sqlite'),
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        #overrides the default config with values taken from the config file
        app.config.from_pyfile('config.py',silent=True)
    else:
        #load the test config if passed in
        #to pass test config independentlyof any development values
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        #Flask doesn't create the instance folder automatically
        #but it needs to be created to store files
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello
    @app.route('/hello')
    def hello():
        return "Hello David"

    #Initialize Database
    db.init_app(app)

    #register auth blueprint in the application
    app.register_blueprint(auth.bp)

    return app
