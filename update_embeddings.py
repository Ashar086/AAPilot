from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openai
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = environ.get('OPENAI_API_KEY')

app = Flask(__name__)

# Database configuration
DB_USER = environ.get('DB_USER', 'root')
DB_PASSWORD = environ.get('DB_PASSWORD', 'Ashar.123')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_NAME = environ.get('DB_NAME', 'aa_pilot')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    embeddings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
            model="text-embedding-ada-002"
        )
        
        # Extract the embedding vector
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f'Error generating embeddings: {e}')
        return None

def update_embeddings():
    with app.app_context():
        # Get all answers without embeddings
        answers = UserAnswer.query.filter(UserAnswer.embeddings.is_(None)).all()
        print(f"Found {len(answers)} records without embeddings")
        
        for answer in answers:
            try:
                print(f"Processing answer ID: {answer.id}")
                embeddings = generate_embeddings(answer.answers)
                if embeddings:
                    answer.embeddings = embeddings
                    db.session.commit()
                    print(f"Updated embeddings for answer ID: {answer.id}")
                else:
                    print(f"Failed to generate embeddings for answer ID: {answer.id}")
            except Exception as e:
                print(f"Error processing answer ID {answer.id}: {e}")
                db.session.rollback()

if __name__ == '__main__':
    update_embeddings()
    print("Embedding update process completed")
