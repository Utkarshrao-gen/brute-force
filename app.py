from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from inception_model import get_prediction
import os
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')  # returns the landing page for image upload


@app.route('/', methods=['GET', 'POST'])
def img_upload():
    if request.method == 'POST':
        file = request.files['file']
        # get the filename
        filename = secure_filename(file.filename)

        photo = Image.open(file)
        photo = photo.resize((299, 299))
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(path) # save the image
        prediction = get_prediction(path)  # predict the presence of the probable object
        os.remove(path)  # delete the image from local storage

    return prediction[0][1]


if __name__ == '__main__':
    app.run(debug=True)
