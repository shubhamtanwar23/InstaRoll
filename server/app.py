from face_recognition import FaceRecognition
import os
import numpy as np
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg',])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


face = FaceRecognition()


def generate_encoding(img_path, name='', use='send'):
    '''
    Return a json object having encoding and location of each face in the image or store them
    or return them according to 'use' parameter

    '''
    # Reading the image
    img = cv2.imread(img_path)

    # Face recongnition API calling 
    all_face_encodings = face.face_encodings(img)
    all_face_locations = face.face_locations(img)
    
    if use == 'send':
        # Generating the data to send back
        face_enc_loc = {}
        for i, e_l in enumerate(zip(all_face_encodings, all_face_locations)):
            face_enc_loc['face {}'.format(i+1)] = {'encoding' : e_l[0].tolist(), 'location' : e_l[1]} 
        return jsonify(face_enc_loc)

    elif use == 'save':
        # Only for single face for now
        np.save(UPLOAD_FOLDER+name, all_face_encodings[0])
    
    else:
        all_faces = recognise_faces(all_face_encodings)
        for (top, right, bottom, left), name in zip(all_face_locations, all_faces):

            # Draw a box around the face
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imwrite(img_path, img)
        return all_faces

def recognise_faces(img_enc):
    '''
    '''
    saved_enc, saved_label = read_save_encodings()
    face_names = []

    for face_encoding in img_enc:
        # See if the face is a match for the known face(s)
        match = face.compare_faces(saved_enc, face_encoding)
        name = "Unknown"
        
        for i, m in enumerate(match): 
            if m :
                name = saved_label[i]

        face_names.append(name)
    return face_names

def read_save_encodings():
    '''
    Read all the encodings saved in the disk and send them 
    '''
    all_encodings = []
    all_labels = []
    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith('.npy'):
            encoding = np.load(UPLOAD_FOLDER + file)
            label = file.rsplit('.')[0]
            all_encodings.append(encoding)
            all_labels.append(label)
    return all_encodings, all_labels

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main_page():
    return '''
            <!doctype html>
                <body>
                    <h1> Welcome to face recognition api</h1>
                </body>
            </html>
                '''


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        name = request.form['name']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('upload_file',
            #                        filename=filename))

            # If we would like to send the data in json format
            # return generate_encoding(UPLOAD_FOLDER+filename, use='send')
            
            # If we wnat to save the encoding of face on server then
            generate_encoding(UPLOAD_FOLDER+filename, use='save', name=name)
            return redirect('/uploaded', 200)
                                    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new Student picture</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=text placeholder="Student name" name="name">
         <input type=submit value=Upload action=>
    </form>
    '''
@app.route('/uploaded')
def file_uploaded():
    return "<h1>File successfully uploaded. </h1>"

@app.route('/verify', methods=['GET', 'POST'])
def verification():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload picture to recognise faces</h1>
        <form method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload action=>
        </form>
        '''
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('upload_file',
            #                        filename=filename))

            # If we would like to send the data in json format
            # return generate_encoding(UPLOAD_FOLDER+filename, use='send')
            
            # If we wnat to save the encoding of face on server then
            names = generate_encoding(UPLOAD_FOLDER+filename, use='ret')
            return render_template('verify.html', names=names, filename=filename)

@app.route('/show/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run()