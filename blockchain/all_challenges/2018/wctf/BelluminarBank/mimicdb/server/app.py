# ~*~ coding: utf-8 ~*~
import os
from flask import Flask, url_for, redirect, render_template, request, send_from_directory

import flask_admin as admin
import flask_login as login

from views import AdminIndexView, BlankView
from user import User

# Create Flask application
app = Flask(__name__)

# bower_components
@app.route('/bower_components/<path:path>')
def send_bower(path):
    return send_from_directory(os.path.join(app.root_path, 'bower_components'), path)

@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory(os.path.join(app.root_path, 'dist'), path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(app.root_path, 'js'), path)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'ajsdlkjqwoiejoikajs9789812dlkjoiqw1'

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

# Flask views
@app.route('/')
def index():
    return render_template("sb-admin/redirect.html")

# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, 
    'Belluminar', 
    index_view=AdminIndexView())
#admin.add_view(BlankView(name='Blank', url='blank', endpoint='blank'))

if __name__ == '__main__':
    print 'Starting'
    app.run(host='0.0.0.0')
