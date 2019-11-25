from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex


class CameraModel(QAbstractListModel):
    def __init__(self, *args, cameras=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cameras = cameras or []

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.cameras[index.row()]

    def rowCount(self, parent=QModelIndex(), **kwargs):
        return len(self.cameras)

    def setData(self, index, value, role=None):
        self.cameras[index.row()] = value
        print(self.cameras)
        self.dataChanged(index, index, [])
