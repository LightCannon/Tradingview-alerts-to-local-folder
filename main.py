from PySide2 import QtCore, QtGui, QtWidgets, QtSerialPort
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import subprocess 
from pyngrok import conf, ngrok
from traceback import print_exc

from flask import Flask
from flask import request, jsonify
from flask_classful import FlaskView, route
import os
import sys
import threading
from mainui import MainWindow
from dotenv import load_dotenv



BASE = 'local'
ROUTE = 'webhooks/csv'
class QuotesView(FlaskView):
    def __init__(self):
        self.events=None

    @route(f'/{ROUTE}', methods=['POST'])
    def save_csv_notification(self):
        payload = request.json
        if payload is None:
            print("Cannot parse the notification request")
            return "Cannot parse the notification request"
        
        content = payload.get('content')
        if content is None:
            print("No content key in the notificaiton body")
            return "No content key in the notificaiton body"

        name = str(mainwin.base_id+1).zfill(9)
        path = os.path.join('.' if mainwin.WEBOOK_FOLDER is None else mainwin.WEBOOK_FOLDER, f'{name}.csv')
        with open(path, 'w') as fcsv:
            fcsv.write(content)
            print(f"Added: {path}")
        
        mainwin.base_id += 1
        return jsonify(message="OK"), 200

class FlaskCore(QtCore.QObject):
    def __init__(self):
        super(FlaskCore, self).__init__()
        self.app = Flask(__name__)
        self.app.config["DEBUG"] = True

        # self.events = OurEvents()

        #print(self.app)
        self.QuotesView = QuotesView()
        self.QuotesView.register(self.app ,route_base=f'/{BASE}')
        #self.QuotesView.events.event_came.connect(spareslot)

    def start(self):
        kwargs = {'host': '127.0.0.1', 'port': PORT , 'threaded' : True, 'use_reloader': False, 'debug':False}
        threading.Thread(target=self.app.run, daemon = True, kwargs=kwargs).start()

if __name__ == "__main__":
    load_dotenv()
    appflask = Flask(__name__)
    
    # ngrok tunnel
    PORT = int(os.getenv('Port'))
    NGROK_AUTH = os.getenv('NgrokToken') 
    conf.get_default().ngrok_path = os.getenv('NgrokEXE') 
    ngrok.set_auth_token(NGROK_AUTH)
    tunnel = ngrok.connect(PORT, "http")
    
    webhook_url = '/'.join([tunnel.data['public_url'], BASE, ROUTE])
    
    app = QtWidgets.QApplication(sys.argv)
    mainwin = MainWindow(tunnel, webhook_url)

    FlaskCore_ =FlaskCore()
    FlaskCore_.start()
    mainwin.show()
    sys.exit(app.exec_())


