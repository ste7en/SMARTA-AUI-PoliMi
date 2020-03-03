from flask import Flask, request, render_template, redirect, url_for
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


@app.route('/api/', methods=['POST', 'GET'])
def api():
    return config_page()


@app.route('/api/<command>')
def api_command(command):
    if command == 'start':
        start()
        return 'Start'
    if command == 'stop':
        stop()
        return 'Stop'


@app.route('/api/config/set_param', methods=['post'])
def set_param():
    if request.method == 'POST':
        minutes = int(request.form['duration_min'])
        seconds = int(request.form['duration_sec'])
        Smarta.set_turn_duration(minutes*60 + seconds)
    else:
        logging.error('Invalid HTTP request. Expected: POST, Found: ' + str(request.method))
    return redirect(url_for('api'))


def config_page():
    minutes = int(Smarta.get_turn_duration() / 60)
    seconds = Smarta.get_turn_duration() % 60
    return render_template('SetParameters.html', default_mins=minutes, default_secs=seconds)


def start_page():
    return render_template('OverlapPage.html')
