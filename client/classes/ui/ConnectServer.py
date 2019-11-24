from ipaddress import ip_address
from PyQt5.QtWidgets import QDialog
from classes.ui.designer.connect_server import Ui_Dialog


class ConnectServer(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_ok.clicked.connect(self.terminate)
        self.ui.lineEdit_ip.textEdited.connect(self.check_input)

    def terminate(self):
        if self.ui.lineEdit_ip.text():
            self.close()
        else:
            self.ui.pushButton_ok.setDisabled(True)
            self.ui.lineEdit_ip.setStyleSheet("border-radius: 5px; border-width: 2px; border-color: #DB2828; border-style: solid;")

    def check_input(self, input):
        try:
            ip_address(input)
            self.ui.lineEdit_ip.setStyleSheet("border-radius: 5px; border-width: 2px; border-color: green; border-style: solid;")
            self.ui.pushButton_ok.setEnabled(True)
        except:
            self.ui.lineEdit_ip.setStyleSheet("border-radius: 5px; border-width: 2px; border-color: #DB2828; border-style: solid;")

    @staticmethod
    def get_ip():
        dialog = ConnectServer()
        dialog.exec_()
        return dialog.ui.lineEdit_ip.text()