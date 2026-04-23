from flask import Blueprint, request, jsonify

progress_bp = Blueprint('progress', __name__)

# Simulated data structure to hold user progress
user_progress = {}  # user_id: {lesson_id: {'score': 0, 'completed': False}}

@progress_bp.route('/progress/<user_id>', methods=['GET'])
def get_user_progress(user_id):
    """Get user progress across all lessons."""
    progress = user_progress.get(user_id, {})
    return jsonify(progress), 200

@progress_bp.route('/progress/<user_id>/score', methods=['POST'])
def calculate_score(user_id):
    """Calculate scores based on lesson submissions."""
    data = request.json
    lesson_id = data.get('lesson_id')
    score = data.get('score')
    if user_id not in user_progress:
        user_progress[user_id] = {}
    user_progress[user_id][lesson_id] = user_progress[user_id].get(lesson_id, {'score': 0, 'completed': False})
    user_progress[user_id][lesson_id]['score'] += score
    return jsonify({'score': user_progress[user_id][lesson_id]['score']}), 200

@progress_bp.route('/progress/<user_id>/completion', methods=['POST'])
def track_completion(user_id):
    """Track lesson completion status."""
    data = request.json
    lesson_id = data.get('lesson_id')
    if user_id not in user_progress:
        user_progress[user_id] = {}
    user_progress[user_id][lesson_id] = user_progress[user_id].get(lesson_id, {'score': 0, 'completed': False})
    user_progress[user_id][lesson_id]['completed'] = True
    return jsonify({'completed': True}), 200

@progress_bp.route('/progress/<user_id>/submit', methods=['POST'])
def lesson_submission(user_id):
    """Handle lesson submission results."""
    data = request.json
    lesson_id = data.get('lesson_id')
    score = data.get('score')
    # Here would be logic to handle the submission, possibly updating the progress
    calculate_score(user_id)
    track_completion(user_id)
    return jsonify({'message': 'Submission successful'}), 200

# The blueprint has to be registered in your main application file
