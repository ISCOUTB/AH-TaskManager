from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    #project config
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///taskManagerDB.db"
    )

    db.init_app(app)

    #Blueprint register
    from . import taskManager
    app.register_blueprint(taskManager.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        db.create_all()
    
    return app
    