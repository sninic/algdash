from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from os import path
from sqlalchemy.ext.automap import automap_base
import timeago, datetime, html
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "algdash"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="sninic2",
    password="Cavalier04.anywhere",
    hostname="sninic2.mysql.pythonanywhere-services.com",
    databasename="sninic2$algdash",
)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bruh'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.context_processor
    def utility_processor():
        def timeAgo(date):
            return timeago.format(date,datetime.datetime.now())
        def leftPos(idx, size):
            return str(idx * size)+"px"
        def unEscape(s):
            return html.unescape(s)
        return dict(timeAgo=timeAgo, leftPos=leftPos, unEscape=unEscape)
    
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    return app
