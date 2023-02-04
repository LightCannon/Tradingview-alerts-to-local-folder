import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QClipboard
from PySide2.QtCore import Qt
from ui import Ui_MainWindow as ui
from pyngrok import ngrok
import os
import dotenv

BASE = 'local'
ROUTE = 'webhooks/csv'

class MainWindow(QMainWindow):
    def __init__(self, ngrok_tunnel, webhook_url):
        super().__init__()
        self.ui = ui()
        self.ui.setupUi(self)
        self.WEBOOK_FOLDER = None
        self.ui.label_4.setText(webhook_url)
        self.setFixedWidth(657)
        self.setFixedHeight(430)

        self.tunnel = ngrok_tunnel
        
        # Create the button for browsing to a folder
        self.ui.pushButton.clicked.connect(self.browse_folder)
        self.ui.pushButton_2.clicked.connect(self.ngrok_change_token)
        self.ui.btn_copy.clicked.connect(self.copy_webhook)

        self.setWindowTitle("Tradingview alerts to local folder")
        # self.ui.label.setText("Tradingview alerts to local folder")
        self.ui.toolButton.setToolTip("Note: you need to provide this token the first time you run this app.\nAfter that it will be save, and you will need to restore only if you change the tunnel service provider.")
        self.show()
    
    def ngrok_change_token(self):
        text, ok = QInputDialog.getText(self, 'Auth Token', 'Enter your Auth Token:')
        if not ok or len(text)<6:
            return
        ngrok_process = ngrok.get_ngrok_process()
        ngrok.disconnect(self.tunnel.public_url)
        ngrok.kill()
        
        ngrok.set_auth_token(text)
        PORT = int(os.getenv('Port'))
        tunnel = ngrok.connect(PORT, "http")
        webhook_url = '/'.join([tunnel.data['public_url'], BASE, ROUTE])
        self.ui.label_4.setText(webhook_url)
        dotenv_file = dotenv.find_dotenv()
        os.environ["NgrokToken"] = text
        dotenv.set_key(dotenv_file, "NgrokToken", os.environ["NgrokToken"])
        
    def browse_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder:
            self.WEBOOK_FOLDER = folder
            print(self.WEBOOK_FOLDER)
            
    def copy_webhook(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.label_4.text())
