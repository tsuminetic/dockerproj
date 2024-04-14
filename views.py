from flask import Blueprint, render_template, request,flash, jsonify
from flask_login import login_required,current_user
from models import Note
from app import db
import json
from flask import url_for,redirect


#creating blueprint named views
views = Blueprint('views', __name__)

#creating a route "/" in views aka home page which requires login to access
@views.route('/',methods=['GET','POST'])
@login_required


def home():
    # if user adds note we get the note in a variable called note 
    if request.method=='POST':
        note= request.form.get('note')

        #if note is empty we flash that the note is empty
        if len(note)<1:
            pass

        else:
            # if note isnt empty we create an instance of the class note where data is the note we stored in the last block and user_id is the current users id
            new_note=Note(data=note, user_id=current_user.id)

            #we add the instance to the database and commit
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("index.html", user= current_user)


#we create another route which just takes the post method
@views.route('delete-note', methods=['POST'])
def delete_note():
    
    # we store the note to be deleted in a veriable called note
    note=json.loads(request.data)
    noteId = note['note']
    note = Note.query.get(noteId)
    #if the note exists and if the note's user_id is the same as current users id we delete the note and commit
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})