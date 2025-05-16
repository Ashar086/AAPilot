from flask import render_template, request, jsonify, redirect, url_for
from . import bp
from .utils import generate_embeddings
from .models import UserAnswer
from auth.models import User
from core.database import db

# Route for starting assessment
@bp.route('/start')
def start_assessment():
    return render_template('shared/assessment-start.html')

# Routes for assessment pages
@bp.route('/page/<int:page_number>')
def assessment_page(page_number):
    if 1 <= page_number <= 5:
        return render_template(f'assessment/assessment-page-{page_number}.html')
    return redirect(url_for('core.landing_page'))

# API route for submitting answers
@bp.route('/submit', methods=['POST'])
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
