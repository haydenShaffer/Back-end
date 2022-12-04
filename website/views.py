from flask import Blueprint, render_template, request,flash,jsonify
from flask_login import  login_required, current_user
from .models import Note, Page,Comments
from . import db
import json 

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    
    if request.method == 'POST':
        noteId=request.form.get('noteId')
        print(noteId)
        note= request.form.get('note')
        comment = request.form.get('comment')
        if note:          
            new_note= Note(data=note, user_id =current_user.id, page_id=1,created_by= current_user.first_name)
            db.session.add(new_note)
            db.session.commit()
            flash('Post created', category='success')
        if comment:
            new_comment= Comments( data=comment, user_id=current_user.id ,created_by= current_user.first_name,note_id=noteId)
            db.session.add(new_comment)
            db.session.commit()
            flash('Post created', category='success')
    page= Page.query.get(1)
    return render_template("home.html", this_user=current_user, page=page)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note =json.loads(request.data)
    noteId = note['noteId']
    note= Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/delete-comments', methods=['POST'])
def delete_comments():
    comments =json.loads(request.data)
    commentsId = comments['commentsId']
    comments= Comments.query.get(commentsId)
    if comments:
        if comments.user_id == current_user.id:
            db.session.delete(comments)
            db.session.commit()
    return jsonify({})
