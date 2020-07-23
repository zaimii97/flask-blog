# this file contains all the  information about the database connection and commands executing sql
from flask import g,current_app
import click
import sqlite3
from flask.cli import with_appcontext






def get_db(): # configuring db connection returning a db connection.
    if 'db' not in g:
        g.db =sqlite3.connect(current_app.config["DATABASE"],
                              detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory=sqlite3.Row
    return g.db

def close_db(e=None):  # closing  a db connection
    db = g.pop('db',None)

    if db is not None:
        db.close()


def init_db():  # initializing db
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("initialized the database")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)