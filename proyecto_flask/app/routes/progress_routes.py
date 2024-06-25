from flask import Blueprint, session, jsonify

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/progress')
def progress():
    progress = session.get('progress', 0)
    return jsonify(progress=progress)
