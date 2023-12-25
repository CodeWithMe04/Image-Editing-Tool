# pip install flask
# pip install opencv-python

import os
import cv2
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp','png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processimg(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgprocessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newfilename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", imgprocessed)
            return newfilename
        case "cwebg":
            newfilename = f"static/{filename.split['.'][0]}.webp"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "cpng":
            newfilename = f"static/{filename.split['.'][0]}.png"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "cjpg":
            newfilename = f"static/{filename.split['.'][0]}.jpg"
            cv2.imwrite(newfilename, img)
            return newfilename
    pass

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error 2"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processimg(filename, operation)
            flash(f"Your image has processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0)