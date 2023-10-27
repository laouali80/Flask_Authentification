from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# use the determine if the database exists or not
from os import path

from flask_login import LoginManager

# defining a database object
db = SQLAlchemy()
#DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    # it encrypts or secures the cookies and sessions data relative to our website
    app.config['SECRET_KEY'] = 'any random word/string/setence'
    
    # configuration of the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    # app.app_context().push()
    
    # initialysation of the database
    db.init_app(app)

    
    # .views (from this folder in views)
    from .views import views
    from .auth import auth

    # register our routes to the flask app
    # ulr_prefix='/auth' : it is a pre url path that it is added to our route path. eg: if @auth.route('/home') then i will have to go to /auth/home via get or post will send me there.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # checking if the database is created
    from .models import User, Note

    with app.app_context():
        db.create_all()

    # how to find a user 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # where the user should view if he is not login
    login_manager.init_app(app)

    # how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
