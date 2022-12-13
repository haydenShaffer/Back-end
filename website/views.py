from flask import Blueprint, render_template, request,flash,jsonify, redirect, url_for
from flask_login import  login_required, current_user
from .models import Note, Page,Comments, User
from sqlalchemy import update
from . import db
import json 
from werkzeug.security import generate_password_hash

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    
    if request.method == 'POST':
        noteId=request.form.get('noteId')
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

@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        new_email=request.form.get('new_email')
        print(new_email)
        new_password=request.form.get('new_password')
        new_name=request.form.get('new_name')
        if new_email:
            emailExist = User.query.filter_by(email= new_email.lower()).first()
            if emailExist:
                flash('Account with that email already exists',category='error')
            elif len(new_email)< 4:
                flash('Email is too short!', category='error')
            else:
                user=current_user
                user.email = new_email.lower()
                db.session.commit()
                flash('Email Changed', category='success')
                return redirect(url_for("auth.logout"))
        if new_password:
            if len(new_password)<8:
                flash('Password must be at least 8 characters!', category='error')
            else:    
                user=current_user
                user.password = generate_password_hash(new_password, method='sha256')
                db.session.commit()
                flash('Password Changed', category='success')
                return redirect(url_for("auth.logout"))
        if new_name:
            if len(new_name)< 2:
                flash('First name must be more than 1 character!', category='error')
            else:
                user=current_user
                user.first_name = new_name
                db.session.commit()
                flash('Name Changed', category='success')
                return redirect(url_for("auth.logout"))
    return render_template("account.html", this_user=current_user)

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
