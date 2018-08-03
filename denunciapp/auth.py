#Authentication example Blueprint
#Blueprint -> way to organize related views and code
# rather than registering the view in the application
# they are registered in a blueprint, which is later
# registered in the application

import functools

from flask import (
    Blueprint, flash, g,redirect,render_template,request,session,url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_skeleton.db import get_db

#Blueprint called Auth
#__name__ tells wheres its defined, like the application
#url_prefix will be prepended to all the url associated with the bp
bp=Blueprint('auth',__name__,url_prefix='/auth')

#To register the bp place the new code in the create app function
# from . import auth
# app.register_blueprint(auth.bp)

#associate url with function
@bp.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        db=get_db()
        error=None

        if not username:
            error="Username is required"
        elif not password:
            error="Password is required"
        elif db.execute(
                        "SELECT id FROM user WHERE username= ?",
                        (username,)
                        ).fetchone() is not None:
                            error="User {} is already registered".format(username)

        if error is None:
            db.execute("INSERT INTO user(username,password) VALUES(?,?)",
            (username,generate_password_hash(password)))
            db.commit()
            #url_for -> generate url based on the name
            #it's the prefer method so you don't have to change the linked code when changing the url
            return redirect(url_for('auth.login'))

        #flash -> stores messages that can be retrieved when rendering the template
        flash(error)
    return render_template("auth/register.html")

@bp.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        db=get_db()
        error=None
        user=db.execute("SELECT * FROM user WHERE username=?",(username,)).fetchone()
        if user is None:
            error="Incorrect username"
        #check_password_hash -> hashes and compares passwords
        elif not check_password_hash(user['password'],password):
            error="Invalid password"

        #session -> dict that stores data across requests
        if error is None:
            session.clear()
            session['user_id']=user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#before_app_request-> register a function that runs before the view function no matter wht URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=get_db("Select * FROM user WHERE id=?",(user_id,)).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
