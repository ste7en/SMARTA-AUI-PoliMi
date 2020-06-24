from flask import Flask, request, render_template, redirect, url_for, abort, send_from_directory
from markupsafe import escape
from pygtail import Pygtail
from smarta import Smarta
from smarta import Event
from time import sleep
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s [Thread %(threadName)s)] : %(message)s')
app = Flask(__name__)
application_instance = Smarta()

logging.debug('Flask WebInterface started')


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('./templates/images', path)


def start():
    logging.info('HTTP Client started the application')
    if not application_instance.is_running(): application_instance.start()


def stop():
    logging.info('HTTP Client stopped the application')
    if application_instance.is_running(): application_instance.stop()


@app.route('/about')
@app.route('/index')
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/api/<path:subpath>', methods=['POST', 'GET'])
def api(subpath=None):
    command = escape(subpath)

    if request.method == 'POST':
        if command == 'config/set_param':
            minutes = int(request.form['duration_min'])
            seconds = int(request.form['duration_sec'])
            Smarta.set_turn_duration(minutes * 60 + seconds)
            return '', 204
        if command == 'run/send_overlap':
            application_instance.on_event(Event.VOICE_OVERLAP_DET_EV)
            return '', 204
        else:
            logging.error('Invalid POST request: ' + str(request.url))

    if request.method == 'GET':
        if command == 'start':
            start()
            return redirect(url_for('start_page'))
        if command == 'stop':
            stop()
            return redirect(url_for('summary_page'))
        if command == 'archive':
            return render_template('archive.html')
        if command == 'log':
            return log()
        if command == 'about':
            return redirect(url_for('index'))
        else:
            logging.error('Invalid GET request: ' + str(request.url))

    abort(404)


@app.route('/api/config')
@app.route('/api/config/')
def config_page():
    turn_duration = Smarta.get_turn_duration()
    minutes = int(turn_duration / 60)
    seconds = turn_duration % 60
    return render_template('SetParameters.html', default_mins=minutes, default_secs=seconds)


@app.route('/api/run')
def start_page():
    return render_template('OverlapPage.html')


@app.route('/api/summary')
def summary_page():
    avg_duration, n_turns, n_overlaps = application_instance.get_summary()
    return render_template('summary.html',
                           avg_duration_min=round(avg_duration/60),
                           avg_duration_sec=round(avg_duration % 60),
                           n_turns=n_turns, n_overlaps=n_overlaps)


def log():
    def generate():
        while True:
            for line in Pygtail('../logs/smarta.log'):
                yield line
            sleep(2)

    return app.response_class(generate(), mimetype='text/plain')
