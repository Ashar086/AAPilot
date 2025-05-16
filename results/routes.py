from flask import render_template, jsonify
from . import bp
from .models import UserResult
from assessment.models import UserAnswer

@bp.route('/<user_id>')
def display_results(user_id):
    try:
        # Get user's results from database
        user_result = UserResult.query.filter_by(user_id=user_id).first()
        if user_result:
            return render_template('shared/results.html', results=user_result.result_data)
        return render_template('shared/results.html', error='No results found')
    except Exception as e:
        return render_template('shared/results.html', error=str(e))

@bp.route('/matchability-compare')
def matchability_compare():
    return render_template('shared/result.matchabilityCompare.html')

@bp.route('/share')
def share():
    return render_template('shared/share.html')

@bp.route('/api/<user_id>')
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
