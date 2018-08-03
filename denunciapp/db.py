import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    #g -> special object. Unique for each request Store data accesed by multiple
    #functions in the same request
    if 'db' not in g:
        #current_app -> points to the flask app handling the request
        #sqlite3.connect() -> stablishes the connection to the file
        g.db=sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #sqlite3.Row -> tells the connection to return rows that behave like dicts
        # allows to accessing columns by name
        g.db.row_factory=sqlite3.Row
    return g.db

def close_db(e=None):
    #checks if a connection was created and closes it
    db=g.pop('db',None)
    if db is not None:
        db.close()

def init_db():
    db=get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existent data and create new tables"""
    init_db()
    click.echo("Database Initialized")

def init_app(app):
    # app.teardown_appcontext -> call the function when cleaning up after running the response
    app.teardown_appcontext(close_db)
    # adds new command that can be run with the flask command
    app.cli.add_command(init_db_command)
