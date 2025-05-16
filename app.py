from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from os import environ

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = environ.get('OPENAI_API_KEY')

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Database configuration
    DB_USER = environ.get('DB_USER', 'root')
    DB_PASSWORD = environ.get('DB_PASSWORD', '')
    DB_HOST = environ.get('DB_HOST', 'localhost')
    DB_NAME = environ.get('DB_NAME', 'aa_pilot')

    # MySQL connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    from core.database import db
    db.init_app(app)

    # Register blueprints
    from core import bp as core_bp
    app.register_blueprint(core_bp)

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from assessment import bp as assessment_bp
    app.register_blueprint(assessment_bp, url_prefix='/assessment')

    from results import bp as results_bp
    app.register_blueprint(results_bp, url_prefix='/results')

    from recipient import bp as recipient_bp
    app.register_blueprint(recipient_bp, url_prefix='/recipient')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
