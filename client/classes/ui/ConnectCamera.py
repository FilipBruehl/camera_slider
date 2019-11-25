from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QStringListModel
from classes.ui.designer.connect_camera import Ui_Dialog
from classes.DataContainer import DataContainer, Observer, Subject
from classes.ui.CameraModel import CameraModel


class ConnectCamera(QDialog, Observer):

    def __init__(self, cameras=None):
        super().__init__()
        print("Inside ConnectCamera")
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        DataContainer.get_instance().attach(self)
        self.cameras = cameras or []
        self.model = QStringListModel(self.cameras)
        self.ui.listView_cameras.setModel(self.model)
        self.ui.pushButton_select.clicked.connect(self.close)
        self.selected_index = None
        self.selected_camera = None
        self.ui.listView_cameras.selectionModel().currentChanged.connect(self.on_change)

    def on_change(self, current, prev):
        self.selected_index = current.row()
        self.selected_camera = self.cameras[self.selected_index]
        self.ui.pushButton_select.setEnabled(True)

    @classmethod
    def get_camera(cls):
        dialog = cls()
        dialog.exec_()
        return (dialog.selected_index, dialog.selected_camera)

    def update(self, subject: Subject) -> None:
        print("Inside update in ConnectCamera")
        self.cameras = subject.get_data("cameras")
        print("updated", self.cameras)
        self.model.setStringList(self.cameras)
        print("model updated")
