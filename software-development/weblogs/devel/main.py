from flask import Blueprint, current_app
from . import db
from flask import Flask, redirect, url_for, request, jsonify, render_template, flash, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import magic # To check file type.
import os
import uuid
import subprocess

main = Blueprint('main', __name__)

def allowed_file(file):
   if not magic.from_buffer(file.stream.read(2048), mime = True) == "text/plain":
      flash("Unsupported file format")
      return False
   # Hacer chequeos de tipo de file.
   file.stream.seek(0)
   return True

@main.route('/')
def index():
   return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/graphs')
@login_required
def gen_graphs():
   #checkLogin() 
   return render_template("graphs.html", data = session["file_id"])

@main.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_site():
   if request.method == 'POST':
   # check if the post request has the file part
      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
      file = request.files['file']
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
         flash('No selected file')
         return redirect(request.url)
      if file and allowed_file(file):
         filename = str(uuid.uuid1()) #  secure_filename(file.filename)   # Esto se va a cambiar por un identificador unico en DB.
         session["file_id"] = filename
         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
         subprocess.Popen(["python", "run.py", "%s/%s" % (current_app.config['UPLOAD_FOLDER'], filename)])
         flash("File %s successfuly uploaded" % file.filename)

   return render_template('uploadlog.html', name = "cheo")

@main.route('/logs/', methods = ['POST', 'GET'])
@login_required
def read_logs():
   if request.method == 'POST':
      date = request.form['date']
   else:
      date = request.args.get('date')

   f = open("devel/uplogs/access_log", "r")
   results = []
   for line in f:
      fields = line.split()
      if fields[3][1:-3] == date:
         results.append(line)

   return jsonify(logs = results)