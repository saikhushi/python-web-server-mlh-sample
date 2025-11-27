from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Note, User

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['GET'])
@jwt_required()
def list_notes():
    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notes]), 200

@notes_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title:
        return jsonify({'msg': 'title required'}), 400
    note = Note(user_id=user_id, title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@notes_bp.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first_or_404()
    return jsonify(note.to_dict()), 200

@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first_or_404()
    data = request.get_json() or {}
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    db.session.commit()
    return jsonify(note.to_dict()), 200

@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return jsonify({'msg': 'deleted'}), 200
