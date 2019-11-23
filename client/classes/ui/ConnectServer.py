from PyQt5.QtWidgets import QDialog
from classes.ui.designer.connect_camera import Ui_Dialog


class ConnectServer(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_reset.clicked.connect(self.close)
        self.ui.pushButton_ok.clicked.connect(self.close)

    @staticmethod
    def get_ip():
        dialog = ConnectServer()
        dialog.exec_()
        return dialog.ui.lineEdit_ip.text()