from flask import Flask, request, render_template, redirect, url_for, abort
from markupsafe import escape
from smarta.smarta_fsm import Smarta
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s [Thread %(threadName)s)] : %(message)s')
app = Flask(__name__)
application_instance = Smarta()

logging.debug('Flask WebInterface started')


def start():
    logging.info('HTTP Client started the application')
    application_instance.start()


def stop():
    logging.info('HTTP Client stopped the application')
    application_instance.stop()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/<path:subpath>', methods=['POST', 'GET'])
def api(subpath=None):
    command = escape(subpath)

    if request.method == 'POST':
        if command == 'config/set_param':
            minutes = int(request.form['duration_min'])
            seconds = int(request.form['duration_sec'])
            Smarta.set_turn_duration(minutes * 60 + seconds)
            return '', 204

        else:
            logging.error('Invalid POST request: ' + str(request.url))

    if request.method == 'GET':
        if command == 'start':
            start()
            return redirect(url_for('start_page'))
        if command == 'stop':
            stop()
            return redirect(url_for('stop_page'))

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
def stop_page(avg_duration, n_turns, n_overlaps):
    return render_template('summary.html', avg_duration=avg_duration, n_turns=n_turns, n_overlaps=n_overlaps)