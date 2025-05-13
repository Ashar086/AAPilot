from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
from dotenv import load_dotenv
import openai
import json

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = environ.get('OPENAI_API_KEY')

def generate_embeddings(answers):
    """
    Generate embeddings for user answers using OpenAI's embedding model.
    """
    try:
        # Format answers into a single text string
        formatted_text = ' '.join([f'Q{q}: {a}' for q, a in answers.items()])
        
        # Generate embeddings using OpenAI
        response = openai.Embedding.create(
            input=formatted_text,
            model="text-embedding-ada-002"  # Using the latest embedding model
        )
        
        # Extract the embedding vector
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f'Error generating embeddings: {e}')
        return None

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
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    embeddings = db.Column(db.JSON, nullable=True)  # Store OpenAI embeddings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    result_type = db.Column(db.String(50), nullable=False)
    result_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Ensure all required tables exist
try:
    with app.app_context():
        db.create_all()
        print('Database tables created successfully!')
except Exception as e:
    print(f'Error creating database tables: {e}')

# Route for landing page
@app.route('/')
def landing_page():
    return render_template('landing-page.html')

# Route for starting assessment
@app.route('/assessment/start')
def start_assessment():
    return render_template('assessment-start.html')

# Routes for assessment pages
@app.route('/assessment/page/<int:page_number>')
def assessment_page(page_number):
    if 1 <= page_number <= 5:
        return render_template(f'assessment-page-{page_number}.html')
    return redirect(url_for('landing_page'))

# API route for submitting answers
@app.route('/aa/answers', methods=['POST'])
def submit_answers():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        page_number = data.get('pageNumber')
        answers = data.get('answers')
        
        if not user_id or not answers or not page_number:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create user if not exists
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            user = User(user_id=user_id)
            db.session.add(user)
        
        # Generate embeddings for the answers
        embeddings = generate_embeddings(answers)
        
        # Save answers and embeddings
        user_answer = UserAnswer(
            user_id=user_id,
            page_number=page_number,
            answers=answers,
            embeddings=embeddings
        )
        db.session.add(user_answer)
        db.session.commit()
        
        return jsonify({
            'message': 'Answers submitted successfully',
            'embeddings_generated': embeddings is not None
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API route for getting results
@app.route('/aa/results/<user_id>', methods=['GET'])
def get_results(user_id):
    try:
        # Get all answers for the user
        user_answers = UserAnswer.query.filter_by(user_id=user_id).order_by(
            UserAnswer.page_number,
            UserAnswer.created_at.desc()
        ).all()
        
        if not user_answers:
            return jsonify({'error': 'No results found for this user'}), 404
        
        # Organize answers by page
        results = {}
        for answer in user_answers:
            if answer.page_number not in results:  # Only take the latest answer for each page
                results[answer.page_number] = {
                    'answers': answer.answers,
                    'createdAt': answer.created_at.isoformat()
                }
        
        return jsonify({
            'userId': user_id,
            'pages': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for displaying results
@app.route('/results/<user_id>')
def display_results(user_id):
    try:
        # Get user's results from database
        user_result = UserResult.query.filter_by(user_id=user_id).first()
        if user_result:
            return render_template('results.html', results=user_result.result_data)
        return render_template('results.html', error='No results found')
    except Exception as e:
        return render_template('results.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)