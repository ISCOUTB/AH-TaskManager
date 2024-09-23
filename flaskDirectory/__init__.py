from flask import Flask, render_template

def create_app():

    app = Flask(__name__)

    #project config
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev'
    )

    #Blueprint register
    from . import taskManager
    app.register_blueprint(taskManager.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
    