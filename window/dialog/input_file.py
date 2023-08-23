from PyQt5.Qt import *

from window.ui.dialog_input_file import Ui_Form
import os

class Dialog_input_file(QWidget, Ui_Form):
    dialog_close = pyqtSignal(bool)
    inputs = pyqtSignal(int, str, str)

    def __init__(self, func_num: int, display_dict: dict):
        super().__init__()
        self.func_num = func_num
        self.display_dict = display_dict
        self.setupUi(self)

    def setupUi(self, dialog_window):
        super().setupUi(dialog_window)
        self.toolButton.hide()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(self.display_dict['title'])
        # self.toolButton_file1.setIcon(QIcon("resource/image/file.png"))
        self.toolButton_file.setIcon(QIcon(":/file.png"))
        # 连接信号和槽函数
        self.pushButton_yes.clicked.connect(self.pushButton_yes_event)
        self.pushButton_no.clicked.connect(self.pushButton_no_event)
        self.toolButton_file.clicked.connect(self.toolButton_file_event)

    def pushButton_yes_event(self):
        try:
            if os.path.exists(self.lineEdit.text()):
                self.inputs.emit(self.func_num, self.lineEdit.text(), "")
                self.dialog_close.emit(True)
                self.close()
            else:
                QMessageBox.critical(self, "输入错误", "文件不存在")
        except Exception as e:
            print("Exception in Dialog_input_files --> " + "pushButton_yes_event", e)

    def pushButton_no_event(self):
        try:
            self.dialog_close.emit(False)
            self.close()
        except Exception as e:
            print("Exception in Dialog_input_files --> " + "pushButton_no_event", e)

    def toolButton_file_event(self):
        try:
            file_input, _ = QFileDialog.getOpenFileName(self, '文件选择', './', 'all(*.*);;txt(*.txt);;python(*.py)')
            self.lineEdit.setText(file_input)
        except Exception as e:
            print("Exception in Dialog_input_files --> " + "toolButton_file1_event", e)
