from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user  # current_user is only passe to the render_template of home and login, (signUp)
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(content=note, user_id = current_user.id)

            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user )


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # this 'request.data' is the data sends by the javascript 'noteId'
    # And then json.loads turn it into a python dictionary

    noteId = note['noteId'] # we can then access the noteId in side the data 

    note_delete = Note.query.get(noteId)

    if note:
        if note_delete.user_id == current_user.id:
            db.session.delete(note_delete)
            db.session.commit()
    
    return jsonify({})