from filterize.filterize import Filterize
import cv2
import os
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['RESULT_FOLDER'] = RESULT_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
filterize = Filterize()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    input_type = request.form['a']
    input_type = input_type.split(' ')
    if len(input_type) == 1:
        mode = input_type[0]
    else :
         mode = input_type[0]
         nose_filter = input_type[1]
    print(input_type)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        PATH_IMG= os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(PATH_IMG)
        if mode == 'nose_filter':
            result = filterize.nose_filter(PATH_IMG, nose_filter=nose_filter)
            cv2.imwrite(os.path.join(app.config['RESULT_FOLDER'], filename), result)
            flash('Image successfully uploaded and displayed below')
            return render_template('index.html', filename=filename)
        elif mode == 'cartoon':
            result = filterize.create_cartoon_img(PATH_IMG)
            cv2.imwrite(os.path.join(app.config['RESULT_FOLDER'], filename), result)
            flash('Image successfully uploaded and displayed below')
            return render_template('index.html', filename=filename)

        print('upload_image filename: ' + filename)

        
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='results/' + filename), code=301)

if __name__ == "__main__":
    app.run('localhost',debug=True,port=8989)