"""This module is main module of Loumidis application"""

import os
import tempfile
from werkzeug.utils import secure_filename

from flask import Flask, render_template, redirect, request, flash, url_for, send_from_directory
from flask_restful import Api
from dotenv import load_dotenv

load_dotenv(verbose=True)

from server.api import DataRes, TableRes, ProductRes, ResultRes, ResultListRes
from server.utils import allowed_file
from server.tasks import make_celery
from server.tasks.parse import parse_csv

app = Flask(__name__, static_folder="static", template_folder="template")

SECRET_KEY = os.environ.get("SECRET_KEY", default='powerful secret key')
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", default=None)
CELERY_MAIN = os.environ.get('CELERY_MAIN', default='server.jobs')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND', default='')
CELERY_BROKER = os.environ.get('CELERY_BROKER', default='pyamqp://guest@localhost//')

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

# API entry points
api.add_resource(DataRes, '/api/data/<data_id>',
    resource_class_kwargs={'upload_folder': UPLOAD_FOLDER})
api.add_resource(TableRes, '/api/table')
api.add_resource(ProductRes, '/api/product/<field_name>')
api.add_resource(ResultRes, '/api/result/<data_id>',
    resource_class_kwargs={'upload_folder': UPLOAD_FOLDER})
api.add_resource(ResultListRes, '/api/result')

# celery
app.config.update(
    CELERY_BROKER_URL=CELERY_BROKER,
    CELERY_RESULT_BACKEND=CELERY_BACKEND
)
celery = make_celery(app)

# celery tasks
@celery.task
def parse_task(file_path):
    parse_csv(file_path)

# routing
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('upload_page'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            result = parse_task.delay(file_path)
            return redirect(url_for('upload_page', filename=filename))

    return render_template('upload.html', title='Upload Data', page='upload')


@app.route('/data', methods=['GET'])
def data_page():
    return render_template('data.html', title='Database', page='data')


@app.route('/result', methods=['GET'])
def result_list_page():
    return render_template('result-list.html', title='Results', page='result')


@app.route('/result/<data_id>', methods=['GET'])
def result_page(data_id):
    return render_template('result.html', title='Result', data_id=data_id, page='result')


@app.route('/images/<image_name>', methods=['GET'])
def images_page(image_name):
    return send_from_directory(UPLOAD_FOLDER, image_name)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
