from flask import Flask
from .controller.project_management_controller import auth_bp
from .extensions import init_app as init_db
import  os
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app)
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URI = os.getenv('DATABASE_URL')
    print(SECRET_KEY)
    print(DATABASE_URI)
    app.config.from_object('app.config.Config')

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix='/project')

    return app
