from PyQt5.Qt import *

from window.ui.dialog_input_two import Ui_Form


class Dialog_input_two(QWidget, Ui_Form):
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
        self.label.setText(self.display_dict['label_1'])
        self.label_2.setText(self.display_dict['label_2'])
        # 连接信号和槽函数
        self.pushButton_yes.clicked.connect(self.pushButton_yes_event)
        self.pushButton_no.clicked.connect(self.pushButton_no_event)

    def pushButton_yes_event(self):
        try:
            self.inputs.emit(self.func_num, self.lineEdit.text(), self.lineEdit_2.text())
            self.dialog_close.emit(True)
            self.close()
        except Exception as e:
            print("Exception in Dialog_input_two --> " + "pushButton_yes_event", e)

    def pushButton_no_event(self):
        try:
            self.dialog_close.emit(False)
            self.close()
        except Exception as e:
            print("Exception in Dialog_input_two --> " + "pushButton_no_event", e)

