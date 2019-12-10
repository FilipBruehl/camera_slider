from ipaddress import ip_address
from PyQt5.QtWidgets import QDialog
from classes.ui.designer.connect_server import Ui_Dialog
from styles.Styles import ConnectServerStyles


class ConnectServer(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_ok.setStyleSheet(ConnectServerStyles.button_style().toString())
        self.ui.lineEdit_ip.setStyleSheet(ConnectServerStyles.line_edit_style().toString())
        self.ui.pushButton_ok.clicked.connect(self.terminate)
        self.ui.lineEdit_ip.textEdited.connect(self.check_input)

    def terminate(self):
        if self.ui.lineEdit_ip.text():
            self.close()
        else:
            self.ui.pushButton_ok.setDisabled(True)
            self.ui.lineEdit_ip.setProperty("valid", False)
            self.ui.lineEdit_ip.style().unpolish(self.ui.lineEdit_ip)
            self.ui .lineEdit_ip.style().polish(self.ui.lineEdit_ip)
            self.ui.lineEdit_ip.update()

    def check_input(self, input):
        try:
            ip_address(input)
            self.ui.lineEdit_ip.setProperty("valid", True)
            self.ui.lineEdit_ip.style().unpolish(self.ui.lineEdit_ip)
            self.ui.lineEdit_ip.style().polish(self.ui.lineEdit_ip)
            self.ui.lineEdit_ip.update()
            self.ui.pushButton_ok.setEnabled(True)
        except:
            self.ui.pushButton_ok.setDisabled(True)
            self.ui.lineEdit_ip.setProperty("valid", False)
            self.ui.lineEdit_ip.style().unpolish(self.ui.lineEdit_ip)
            self.ui.lineEdit_ip.style().polish(self.ui.lineEdit_ip)
            self.ui.lineEdit_ip.update()

    @staticmethod
    def get_ip():
        dialog = ConnectServer()
        dialog.exec_()
        return dialog.ui.lineEdit_ip.text()