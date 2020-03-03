from flask import Flask, request, render_template
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
    return render_template('SetParameters.html')
    return '''
        <form action="/api/start" method="get">
            <p><input type=submit value=Start>         
        </form>
        <form action="/api/stop" method="get">
            <p><input type=submit value=Stop>         
        </form>
    '''


@app.route('/api/<command>')
def api_command(command):
    if command == 'start':
        start()
        return 'Start'
    if command == 'stop':
        stop()
        return 'Stop'
