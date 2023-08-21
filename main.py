import ctypes
import re
import sys

from PyQt5.Qt import *

from window.ui.main_window import Ui_main_window
from window.dialog.input_file import Dialog_input_file
from window.dialog.mult_input import Dialog_input_two
from window.dialog.mult_input_files import Dialog_input_files
from window.paint.textEditor import CodeEditor
import resource.image.icon_rc

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("InfoD")


class Window(QWidget, Ui_main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output_history = []
        self.operation_history = []
        self.current_step = -1

    def setupUi(self, main_widget):
        super().setupUi(main_widget)
        self.set_icon()
        self.set_qss()
        # 初始化页面信息
        self.page_init()
        # 连接信号和槽函数
        self.toolButton_back.clicked.connect(self.toolButton_back_event)
        self.toolButton_ori.clicked.connect(self.toolButton_ori_event)
        self.toolButton_fore.clicked.connect(self.toolButton_fore_event)
        self.toolButton_import.clicked.connect(self.toolButton_import_event)
        self.toolButton_export.clicked.connect(self.toolButton_export_event)
        self.toolButton_change.clicked.connect(self.toolButton_change_event)
        # self.comboBox_1.currentIndexChanged.connect(self.comboBox_1_event)
        # self.comboBox_2.currentIndexChanged.connect(self.comboBox_2_event)
        # self.comboBox_3.currentIndexChanged.connect(self.comboBox_3_event)
        # self.comboBox_4.currentIndexChanged.connect(self.comboBox_4_event)
        self.comboBox_1.activated[int].connect(self.comboBox_1_event)
        self.comboBox_2.activated[int].connect(self.comboBox_2_event)
        self.comboBox_3.activated[int].connect(self.comboBox_3_event)
        self.comboBox_4.activated[int].connect(self.comboBox_4_event)

    def page_init(self):
        try:
            self.label_step.setText("")
            self.label_error.setText("")
            self.plainTextEdit_input = CodeEditor(self.widget_left)
            self.plainTextEdit_input.setObjectName("plainTextEdit_input")
            self.gridLayout_3.addWidget(self.plainTextEdit_input, 0, 0, 1, 1)
            self.plainTextEdit_input.setPlaceholderText("输入文本")
            self.plainTextEdit_output.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.plainTextEdit_input.setFocus()
        except Exception as e:
            print("Exception in main --> " + "page_init", e)

    # 设置qss
    def set_qss(self):
        # 设置下拉框固定宽度
        self.comboBox_1.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_2.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_3.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_4.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        # 设置tooltips
        for index in range(self.comboBox_1.count()):
            self.comboBox_1.setItemData(index, self.comboBox_1.itemText(index), role=Qt.ToolTipRole)
        for index in range(self.comboBox_2.count()):
            self.comboBox_2.setItemData(index, self.comboBox_2.itemText(index), role=Qt.ToolTipRole)
        for index in range(self.comboBox_3.count()):
            self.comboBox_3.setItemData(index, self.comboBox_3.itemText(index), role=Qt.ToolTipRole)
        for index in range(self.comboBox_4.count()):
            self.comboBox_4.setItemData(index, self.comboBox_4.itemText(index), role=Qt.ToolTipRole)
        pass

    # 设置图标
    def set_icon(self):
        # self.icon_back = QIcon("resource/image/back.png")
        # self.icon_go = QIcon("resource/image/go.png")
        # self.icon_import = QIcon("resource/image/import.png")
        # self.icon_export = QIcon("resource/image/export.png")
        # self.icon_reset = QIcon("resource/image/reset.png")
        # self.icon_change = QIcon("resource/image/change.png")
        self.icon_back = QIcon(":/back.png")
        self.icon_go = QIcon(":/go.png")
        self.icon_import = QIcon(":/import.png")
        self.icon_export = QIcon(":/export.png")
        self.icon_reset = QIcon(":/reset.png")
        self.icon_change = QIcon(":/change.png")
        # 设置图标
        self.toolButton_back.setIcon(self.icon_back)
        self.toolButton_fore.setIcon(self.icon_go)
        self.toolButton_import.setIcon(self.icon_import)
        self.toolButton_export.setIcon(self.icon_export)
        self.toolButton_ori.setIcon(self.icon_reset)
        self.toolButton_change.setIcon(self.icon_change)
        # self.label.setPixmap(QPixmap('resource/image/deal.png'))
        self.label.setPixmap(QPixmap(':/deal.png'))
        self.label.setScaledContents(True)

    # 功能函数
    # 功能选择槽函数
    def comboBox_1_event(self, func_index):
        try:
            # func_index = self.comboBox_1.currentIndex()
            if func_index == 0:
                print("文本操作类")
            elif func_index == 1:
                self.func_remove_same_line()
                self.label_step.setText("执行功能：行去重")
            elif func_index == 2:
                string_input, status = QInputDialog.getText(self, '行首字符', '请输入行首增加的字符串：')
                if status:
                    self.func_add_start_str(string_input)
                    self.label_step.setText("执行功能：行首符号增加")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 3:
                string_input, status = QInputDialog.getText(self, '行首字符', '请输入行首去除的字符串：')
                if status:
                    self.func_remove_start_str(string_input)
                    self.label_step.setText("执行功能：行首符号去除")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 4:
                string_input, status = QInputDialog.getText(self, '行尾字符', '请输入行尾增加的字符串：')
                if status:
                    self.func_add_end_str(string_input)
                    self.label_step.setText("执行功能：行尾符号增加")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 5:
                string_input, status = QInputDialog.getText(self, '行尾字符', '请输入行尾去除的字符串：')
                if status:
                    self.func_remove_end_str(string_input)
                    self.label_step.setText("执行功能：行尾符号去除")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 6:
                self.func_add_url_head()
                self.label_step.setText("执行功能：url头部http协议增加")
            elif func_index == 7:
                self.func_remove_url_head()
                self.label_step.setText("执行功能：url头部http/https协议去除")
            elif func_index == 8:
                self.func_remove_sub_domain()
                self.label_step.setText("执行功能：去掉一层子域名")
            elif func_index == 9:
                self.func_add_tail_port()
                self.label_step.setText("执行功能：行尾添加默认端口号")
            elif func_index == 10:
                string_input, status = QInputDialog.getText(self, '前加字符', '请输入要插入的字符串：')
                if status:
                    self.func_insert_string_ahead(string_input)
                    self.label_step.setText("执行功能：每个字符前插入指定字符串")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 11:
                string_input, status = QInputDialog.getText(self, '后加字符', '请输入要插入的字符串：')
                if status:
                    self.func_insert_string_tail(string_input)
                    self.label_step.setText("执行功能：每个字符后插入指定字符串")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 12:
                display_dict = {"title": "每行指定位置插入指定字符串", "label_1": "位置：", "label_2": "字符："}
                self.pop_dialog(1, display_dict)
                # string_input_1, string_input_2 =
                # self.func_insert_string_position(string_input_1, string_input_2)
                # self.label_step.setText("执行功能：每行指定位置插入指定字符串")
            elif func_index == 13:
                self.func_extract_port()
                self.label_step.setText("执行功能：提取所有端口号")
            elif func_index == 14:
                self.func_remove_port()
                self.label_step.setText("执行功能：去除所有端口号")
            elif func_index == 15:
                self.func_string_to_ascii()
                self.label_step.setText("执行功能：进行ASCII编码转换")
            elif func_index == 16:
                self.func_replace_space_to_break()
                self.label_step.setText("执行功能：逗号转为换行")
            elif func_index == 17:
                self.func_remove_break()
                self.label_step.setText("执行功能：剔除换行")
            elif func_index == 18:
                self.func_remove_space()
                self.label_step.setText("执行功能：剔除空格")
        except Exception as e:
            print("Exception in main --> " + "comboBox_1_event", e)

    def comboBox_2_event(self, func_index):
        try:
            # func_index = self.comboBox_2.currentIndex()
            if func_index == 0:
                print("文本筛选类")
            elif func_index == 1:
                string_input, status = QInputDialog.getText(self, '去除指定字符串所在行', '指定的字符串：')
                if status:
                    self.func_remove_special_str(string_input)
                    self.label_step.setText("执行功能：去除指定字符串所在行")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 2:
                string_input, status = QInputDialog.getText(self, '提取指定字符串所在行', '指定的字符串：')
                if status:
                    self.func_extract_str(string_input)
                    self.label_step.setText("执行功能：提取指定字符串所在行")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 3:
                display_dict = {"title": "去除多个指定字符串所在行"}
                self.dialog_input = Dialog_input_file(3, display_dict)
                self.dialog_input.dialog_close.connect(self.dialog_close_event)
                self.dialog_input.inputs.connect(self.dialog_return_event)
                self.dialog_input.show()
                self.label_step.setText("执行功能：去除多个指定字符串所在行")
                # if status:
                #     self.func_remove_mult_special_str(string_input)
                #     self.label_step.setText("执行功能：去除多个指定字符串所在行")
                # else:
                #     self.label_error.setText("info：用户取消操作")
            elif func_index == 4:
                display_dict = {"title": "提取多个指定字符串所在行"}
                self.dialog_input = Dialog_input_file(4, display_dict)
                self.dialog_input.dialog_close.connect(self.dialog_close_event)
                self.dialog_input.inputs.connect(self.dialog_return_event)
                self.dialog_input.show()
                self.label_step.setText("执行功能：提取多个指定字符串所在行")
            elif func_index == 5:
                self.func_remove_void_str()
                self.label_step.setText("执行功能：去除无效行")
        except Exception as e:
            print("Exception in main --> " + "comboBox_2_event", e)

    def comboBox_3_event(self, func_index):
        try:
            # func_index = self.comboBox_3.currentIndex()
            if func_index == 0:
                print("信息提取类")
            elif func_index == 1:
                self.func_get_property()
                self.label_step.setText("执行功能：提取完整有效资产(有协议有端口)")
            elif func_index == 2:
                self.func_get_property_domain()
                self.label_step.setText("执行功能：提取资产的域名部分(无协议无端口)")
            elif func_index == 3:
                string_input, status = QInputDialog.getText(self, '提取每行前n个字符', '前n个字符：')
                if status:
                    self.func_get_head_str(string_input)
                    self.label_step.setText("执行功能：提取每行前n个字符")
                else:
                    self.label_error.setText("info：用户取消操作")
            elif func_index == 4:
                # self.func_get_same_line()
                display_dict = {"title": "提取两文件相同行"}
                self.dialog_input = Dialog_input_files(2, display_dict)
                self.dialog_input.dialog_close.connect(self.dialog_close_event)
                self.dialog_input.inputs.connect(self.dialog_return_event)
                self.dialog_input.show()
                self.label_step.setText("执行功能：提取两文件相同行")
            elif func_index == 5:
                self.func_get_root_domain()
                self.label_step.setText("执行功能：提取根域名")
        except Exception as e:
            print("Exception in main --> " + "comboBox_3_event", e)

    def comboBox_4_event(self, func_index):
        try:
            # func_index = self.comboBox_4.currentIndex()
            if func_index == 0:
                print("结果处理类")
            elif func_index == 1:
                # self.func_get_fscan_result()
                pass
                self.label_step.setText("执行功能：fscan提取有效结果")
            elif func_index == 2:
                # self.func_convert_hb_cookie()
                pass
                self.label_step.setText("执行功能：hb转换Cookie格式")
            elif func_index == 3:
                # self.func_remove_ehole_blank()
                pass
                self.label_step.setText("执行功能：棱洞去除干扰行")
        except Exception as e:
            print("Exception in main --> " + "comboBox_4_event", e)

    def pop_dialog(self, func_num, display_dict):
        try:
            self.dialog_input = Dialog_input_two(func_num, display_dict)
            self.dialog_input.dialog_close.connect(self.dialog_close_event)
            self.dialog_input.inputs.connect(self.dialog_return_event)
            self.dialog_input.show()
        except Exception as e:
            print("Exception in main --> " + "pop_dialog", e)

    # 槽函数
    def toolButton_fore_event(self):
        try:
            if self.current_step < len(self.operation_history) - 1:
                self.current_step += 1
                self.label_step.setText("历史操作：" + self.operation_history[self.current_step])
                self.plainTextEdit_output.setPlainText(self.output_history[self.current_step])
            else:
                self.label_error.setText("error：当前已是最新操作")
        except Exception as e:
            print("Exception in main --> " + "toolButton_fore_event", e)

    def toolButton_ori_event(self):
        try:
            self.comboBox_1.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)
            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)
            self.label_error.setText("用户操作：重置功能选项")
        except Exception as e:
            print("Exception in main --> " + "toolButton_ori_event", e)

    def toolButton_back_event(self):
        try:
            if self.current_step > 0:
                self.current_step -= 1
                self.label_step.setText("历史结果：" + self.operation_history[self.current_step])
                self.plainTextEdit_output.setPlainText(self.output_history[self.current_step])
            else:
                self.label_error.setText("error：当前无历史操作")
        except Exception as e:
            print("Exception in main --> " + "toolButton_back_event", e)

    def toolButton_import_event(self):
        try:
            # fd = QFileDialog(self, '文件选择', './', 'all(*.*);;images(*.png *.jpg);;python(*.py)')
            # fd.setAcceptMode(QFileDialog.AcceptOpen)
            # fd.show()
            file_input, _ = QFileDialog.getOpenFileName(self, '文件选择', './', 'all(*.*);;txt(*.txt);;python(*.py)')
            with open(file_input, "r", encoding="utf-8") as f:
                self.plainTextEdit_input.setPlainText(f.read())
                self.label_error.setText("导入文件：" + file_input)
        except Exception as e:
            print("Exception in main --> " + "toolButton_import_event", e)

    def toolButton_export_event(self):
        try:
            file_output, _ = QFileDialog.getSaveFileName(self, "文件保存", "./", "All Files (*);;Text Files (*.txt)", "Text Files (*.txt)")
            with open(file_output, "w", encoding="utf-8") as f:
                f.write(self.plainTextEdit_output.toPlainText())
                self.label_error.setText("导出文件：" + file_output)
        except Exception as e:
            print("Exception in main --> " + "toolButton_export_event", e)

    def toolButton_change_event(self):
        try:
            self.plainTextEdit_input.setPlainText(self.plainTextEdit_output.toPlainText())
            self.plainTextEdit_output.setPlainText("")
            self.label_error.setText("用户操作：输出转换为输入")
        except Exception as e:
            print("Exception in main --> " + "toolButton_change_event", e)

    # 结果返回槽函数
    def dialog_close_event(self, status: bool):
        if not status:
            self.label_error.setText("info：用户取消操作")

    def dialog_return_event(self, func_num, input_1, input_2):
        try:
            if func_num == 1:
                self.func_insert_string_position(int(input_1), input_2)
                self.label_step.setText("执行功能：每行第%s插入字符串%s" % (input_1, input_2))
            elif func_num == 2:
                self.func_get_same_line(input_1, input_2)
                self.label_step.setText("执行功能：提取文件%s和%s相同行" % (input_1, input_2))
            elif func_num == 3:
                self.func_remove_mult_special_str(input_1)
                self.label_step.setText("执行功能：去除多个指定字符串所在行")
            elif func_num == 4:
                self.func_extract_mult_str(input_1)
                self.label_step.setText("执行功能：提取多个指定字符串所在行")
            else:
                print("error!")
                self.label_error.setText("Error!")
        except Exception as e:
            print("Exception in main --> " + "dialog_return_event", e)

    # 功能函数
    # 行去重 1
    def func_remove_same_line(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = {}.fromkeys(lines).keys()
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("行去重")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_same_line", e)

    # 行首符号增加 2
    def func_add_start_str(self, string_tmp):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    line = '%s' % string_tmp + line
                    list_tmp.append(line)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("行首符号增加")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_add_start_str", e)

    # 行首符号去除 3
    def func_remove_start_str(self, string_tmp):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if line.startswith(string_tmp):
                        line_tmp = line.replace(string_tmp, '', 1)
                    else:
                        line_tmp = line
                    list_tmp.append(line_tmp)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("行首符号去除")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_start_str", e)

    # 行尾符号增加 4
    def func_add_end_str(self, string_tmp):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if line.endswith('\n'):
                        line = line.rstrip('\n') + '%s\n' % string_tmp
                    else:
                        line = line + '%s\n' % string_tmp
                    list_tmp.append(line)
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("行尾符号增加")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_add_end_str", e)

    # 行尾符号去除 5
    def func_remove_end_str(self, string_tmp):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if line.endswith('%s\n' % string_tmp):
                        line = line.rstrip(string_tmp + '/\n')
                    elif line.endswith('%s' % string_tmp):
                        line = line.rstrip(string_tmp)
                    list_tmp.append(line)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("行尾符号去除")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_end_str", e)

    # url头部http/https协议去除 7
    def func_remove_url_head(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if line.startswith('http://'):
                        line_tmp = line.replace('http://', '', 1)
                        list_tmp.append(line_tmp)
                    elif line.startswith('https://'):
                        line_tmp = line.replace('https://', '', 1)
                        list_tmp.append(line_tmp)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("url头部http/https协议去除")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_url_head", e)

    # url头部http协议增加 6
    def func_add_url_head(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if line.startswith('https://'):
                        line_tmp = line.replace('https://', 'http://', 1)
                        list_tmp.append(line_tmp)
                    else:
                        line_tmp = 'http://' + line
                        list_tmp.append(line_tmp)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("url头部http协议增加")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_add_url_head", e)

    # 去掉一层子域名 8
    def func_remove_sub_domain(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                pattern = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+(?::\d{1,5})?'
                for line in lines:
                    domain = re.search(pattern, line)
                    if domain:
                        domain_tmp = domain.group(0)
                        if domain_tmp.startswith('http://'):
                            do = domain_tmp[7:].split('.')
                            domain_end = ''
                            for i in do[1:]:
                                domain_end = domain_end + '.' + i
                            list_tmp.append('http://' + domain_end[1:] + '\n')
                        elif domain_tmp.startswith('https://'):
                            do = domain_tmp[8:].split('.')
                            domain_end = ''
                            for i in do[1:]:
                                domain_end = domain_end + '.' + i
                            list_tmp.append('https://' + domain_end[1:] + '\n')
                        else:
                            do = domain_tmp.split('.')
                            domain_end = ''
                            for i in do[1:]:
                                domain_end = domain_end + '.' + i
                            list_tmp.append(domain_end[1:] + '\n')
                lines = list_tmp
                list_tmp = []
                list_tmp2 = []
                black_suffix = ['html', 'php', 'jsp', 'jspx', 'rar', 'zip', 'exe', 'pdf', 'doc', 'docx', 'avi', 'tmp',
                                'db', 'json', 'xls', 'xlsx', 'jpg', 'png', 'ico', 'img']
                pattern1 = '(?:http(?:s?)://)?[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}(:[0-9]{1,5})?'
                pattern2 = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+(?::\d{1,5})?'
                for line in lines:
                    ip = re.search(pattern1, line)
                    domain = re.search(pattern2, line)
                    if domain:
                        if domain.group(0).split('.')[-1] not in black_suffix:
                            list_tmp.append(domain.group(0) + '\n')
                    elif ip:
                        list_tmp2.append(ip.group(0) + '\n')
                list_tmp = {}.fromkeys(list_tmp).keys()
                list_tmp2 = {}.fromkeys(list_tmp2).keys()
                res = []
                for i in list_tmp:
                    res.append(i)
                for i in list_tmp2:
                    res.append(i)
                self.plainTextEdit_output.setPlainText("".join(res))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("去掉一层子域名")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_sub_domain", e)

    # 行尾添加默认端口号 9
    def func_add_tail_port(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if not line.startswith('http'):
                        if ':' not in line:
                            tmp = line.rstrip().split('/')
                            tmp[0] = tmp[0] + ':80'
                            line = '/'.join(tmp)
                    else:
                        if ':' not in line[7:]:
                            if line.startswith('https://'):
                                tmp = line[8:].rstrip().split('/')
                                tmp[0] = tmp[0] + ':443'
                                line = 'https://' + '/'.join(tmp)
                            elif line.startswith('http://'):
                                tmp = line[7:].rstrip().split('/')
                                tmp[0] = tmp[0] + ':80'
                                line = 'http://' + '/'.join(tmp)
                            else:
                                line = line.rstrip() + ':80'
                    if '.' in line:
                        list_tmp.append(line.rstrip('') + '\n')
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("行尾添加默认端口号")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_add_tail_port", e)

    # 每个字符前插入指定字符串 10
    def func_insert_string_ahead(self, insert_str):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    new_string = ''
                    for str_ori in line.rstrip('\n'):
                        new_string += insert_str + str_ori
                    list_tmp.append(new_string + '\n')
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("每个字符前插入指定字符串")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_insert_string_ahead", e)

    # 每个字符后插入指定字符串 11
    def func_insert_string_tail(self, insert_str):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    new_string = ''
                    for str_ori in line.rstrip('\n'):
                        new_string += str_ori + insert_str
                    list_tmp.append(new_string + '\n')
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("每个字符后插入指定字符串")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_insert_string_tail", e)

    # 每行指定位置插入指定字符串 12
    def func_insert_string_position(self, insert_position, insert_str):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    new_string = line[:insert_position] + insert_str + line[insert_position:]
                    list_tmp.append(new_string + '\n')
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("每行指定位置插入指定字符串")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_insert_string_position", e)

    # 提取所有端口号 13
    def func_extract_port(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                str_tmp = ''
                pattern1 = '(:[0-9]{1,5})+'
                for line in lines:
                    domain = re.search(pattern1, line)
                    if domain:
                        list_tmp.append(int(domain.group(0)[1:]))
                    elif line.startswith('http://'):
                        list_tmp.append(80)
                    elif line.startswith('https://'):
                        list_tmp.append(443)
                list_tmp = {}.fromkeys(list_tmp).keys()
                # 以逗号分隔
                for port in sorted(list_tmp):
                    str_tmp = str_tmp + str(port) + ','
                self.plainTextEdit_output.setPlainText(str_tmp.rstrip(','))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取所有端口号")
                self.output_history.append(str_tmp.rstrip(','))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_extract_port", e)

    # 去除所有端口号 14
    def func_remove_port(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                pattern1 = '(:[0-9]{1,5})+'
                for line in lines:
                    domain = re.search(pattern1, line)
                    if domain:
                        list_tmp.append(line.split(domain.group(0))[0])
                    else:
                        list_tmp.append(line)
                list_tmp = {}.fromkeys(list_tmp).keys()
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("去除所有端口号")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_port", e)

    # 进行ASCII编码 15
    def func_string_to_ascii(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                all_ASCCII = '''!"$%&'()*+,-./0123456789:;<>=?@ABCDEFGHIGKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~# '''
                list_tmp = []
                for line in lines:
                    new_string = ''
                    for str_ori in line.rstrip('\n'):
                        if str_ori in all_ASCCII:
                            new_string += '\\u' + str(ord(str_ori))
                        else:
                            new_string += str_ori
                    list_tmp.append(new_string + '\n')
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("进行ASCII编码")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_string_to_ascii", e)

    # 逗号转为换行 16
    def func_replace_space_to_break(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                str_tmp = input_text.replace(",", "\n")
                self.plainTextEdit_output.setPlainText(str_tmp)
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("逗号转为换行")
                self.output_history.append(str_tmp)
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_replace_space_to_break", e)

    # 剔除换行 17
    def func_remove_break(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                str_tmp = ''
                for i in lines:
                    str_tmp += i
                self.plainTextEdit_output.setPlainText(str_tmp)
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("剔除换行")
                self.output_history.append(str_tmp)
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_break", e)

    # 剔除空格 18
    def func_remove_space(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                str_tmp = input_text.replace(" ", "")
                self.plainTextEdit_output.setPlainText(str_tmp)
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("剔除空格")
                self.output_history.append(str_tmp)
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_space", e)

    # 去除指定字符串所在行 2-1
    def func_remove_special_str(self, string_tmp):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                string = r'^(.*?)%s(.*?)' % string_tmp
                for line in lines:
                    match = re.findall(string, line)
                    if match:
                        list_tmp.append(line)
                for line in list_tmp:
                    lines.remove(line)
                self.plainTextEdit_output.setPlainText("\n".join(lines))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("去除指定字符串所在行")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_special_str", e)

    # 提取指定字符串所在行 2-2
    def func_extract_str(self, string_tmp):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                string = r'^(.*?)%s(.*?)' % string_tmp
                for line in lines:
                    match = re.findall(string, line)
                    if match:
                        list_tmp.append(line)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取指定字符串所在行")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_extract_str", e)

    # 去除多个指定字符串所在行 2-3
    def func_remove_mult_special_str(self, file_name):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                with open(file_name, "r") as f:
                    remove_list = f.readlines()
                list_tmp = [item for item in lines if item not in remove_list]
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("去除多个指定字符串所在行")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_void_str", e)

    # 提取多个指定字符串所在行 2-4
    def func_extract_mult_str(self, file_name):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                with open(file_name, "r") as f:
                    remove_list = f.readlines()
                list_tmp = [item for item in lines if any(substring in item for substring in remove_list)]
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取多个指定字符串所在行")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_void_str", e)

    # 去除无效行 2-5
    def func_remove_void_str(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    if line.strip() != '':
                        list_tmp.append(line)
                self.plainTextEdit_output.setPlainText("\n".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("去除无效行")
                self.output_history.append("\n".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_remove_void_str", e)

    # 提取完整有效资产(有协议有端口) 3-1
    def func_get_property(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                list_tmp2 = []
                black_suffix = ['html', 'php', 'jsp', 'jspx', 'rar', 'zip', 'exe', 'pdf', 'doc', 'docx', 'avi', 'tmp',
                                'db', 'json', 'xls', 'xlsx', 'jpg', 'png', 'ico', 'img']
                pattern1 = '(?:http(?:s?)://)?[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}(:[0-9]{1,5})?'
                pattern2 = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+(?::\d{1,5})?'
                for line in lines:
                    ip = re.search(pattern1, line)
                    domain = re.search(pattern2, line)
                    if domain:
                        if domain.group(0).split('.')[-1] not in black_suffix:  # 由于/xxx/a.txt也会被匹配，加一层过滤
                            list_tmp.append(domain.group(0) + '\n')
                    elif ip:
                        list_tmp2.append(ip.group(0) + '\n')
                list_tmp = {}.fromkeys(list_tmp).keys()
                list_tmp2 = {}.fromkeys(list_tmp2).keys()
                self.plainTextEdit_output.setPlainText("".join(list_tmp) + "".join(list_tmp2))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取完整有效资产(有协议有端口)")
                self.output_history.append("".join(list_tmp) + "".join(list_tmp2))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_get_property", e)

    # 提取资产的域名部分(无协议无端口) 3-2
    def func_get_property_domain(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                list_tmp2 = []
                black_suffix = ['html', 'php', 'jsp', 'jspx', 'rar', 'zip', 'exe', 'pdf', 'doc', 'docx', 'avi', 'tmp',
                                'db', 'json', 'xls', 'xlsx', 'jpg', 'png', 'ico', 'img']
                pattern1 = '(?:http(?:s?)://)?[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}'
                pattern2 = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+'
                for line in lines:
                    if line.startswith('http://'):
                        line = line.replace('http://', '', 1)
                    elif line.startswith('https://'):
                        line = line.replace('https://', '', 1)
                    ip = re.search(pattern1, line)
                    domain = re.search(pattern2, line)
                    if domain:
                        if domain.group(0).split('.')[-1] not in black_suffix:
                            list_tmp.append(domain.group(0) + '\n')
                    elif ip:
                        list_tmp2.append(ip.group(0) + '\n')
                list_tmp = {}.fromkeys(list_tmp).keys()
                list_tmp2 = {}.fromkeys(list_tmp2).keys()
                self.plainTextEdit_output.setPlainText("".join(list_tmp) + "".join(list_tmp2))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取资产的域名部分(无协议无端口)")
                self.output_history.append("".join(list_tmp) + "".join(list_tmp2))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_get_property_domain", e)

    # 提取每行前n个字符 3-3
    def func_get_head_str(self, num):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                for line in lines:
                    str_tmp = line[:int(num)].rstrip()
                    list_tmp.append(str_tmp + '\n')
                self.plainTextEdit_output.setPlainText("".join(list_tmp))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取每行前n个字符")
                self.output_history.append("".join(list_tmp))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_get_head_str", e)

    # 提取两文件相同行 3-4
    def func_get_same_line(self, filename1, filename2):
        try:
            list_tmp = []
            with open(filename1, "r", encoding='utf-8') as f1:
                lines1 = f1.readlines()
            with open(filename2, "r", encoding='utf-8') as f2:
                lines2 = f2.readlines()
            for line in lines1:
                if line in lines2:
                    list_tmp.append(line)
            self.plainTextEdit_output.setPlainText("".join(list_tmp))
            if self.current_step != len(self.operation_history) - 1:
                self.operation_history = self.operation_history[:self.current_step + 1]
                self.output_history = self.output_history[:self.current_step + 1]
            self.operation_history.append("提取两文件相同行")
            self.output_history.append("".join(list_tmp))
            self.current_step += 1
            self.label_error.setText("")
        except Exception as e:
            print("Exception in main --> " + "func_get_same_line", e)
            self.label_error.setText("error：读取错误！")

    # 提取根域名 3-5
    def func_get_root_domain(self):
        try:
            input_text = self.plainTextEdit_input.toPlainText()
            if input_text:
                lines = input_text.split("\n")
                list_tmp = []
                key_domain = []
                pattern = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+(?::\d{1,5})?'
                for line in lines:
                    domain = re.search(pattern, line)
                    if domain:
                        try:
                            domain_tmp = domain.group(0)
                            if domain_tmp.startswith('http://'):
                                do = domain_tmp[7:].split('.')
                                domain_end = ''
                                if do[-2] == 'com' or do[-2] == 'org' or do[-2] == 'net':
                                    domain_end = do[-3] + '.' + do[-2] + '.' + do[-1]
                                elif do[-2] == 'gov' or do[-2] == 'edu':
                                    key_domain.append('http://' + domain_tmp + '\n')
                                else:
                                    domain_end = do[-2] + '.' + do[-1]
                                list_tmp.append('http://' + domain_end + '\n')
                            elif domain_tmp.startswith('https://'):
                                do = domain_tmp[8:].split('.')
                                domain_end = ''
                                if do[-2] == 'com' or do[-2] == 'org' or do[-2] == 'net':
                                    domain_end = do[-3] + '.' + do[-2] + '.' + do[-1]
                                elif do[-2] == 'gov' or do[-2] == 'edu':
                                    key_domain.append('https://' + domain_tmp + '\n')
                                else:
                                    domain_end = do[-2] + '.' + do[-1]
                                list_tmp.append('https://' + domain_end + '\n')
                            else:
                                do = domain_tmp.split('.')
                                domain_end = ''
                                if do[-2] == 'com' or do[-2] == 'org' or do[-2] == 'net':
                                    domain_end = do[-3] + '.' + do[-2] + '.' + do[-1]
                                elif do[-2] == 'gov' or do[-2] == 'edu':
                                    key_domain.append(domain_tmp + '\n')
                                else:
                                    domain_end = do[-2] + '.' + do[-1]
                                list_tmp.append(domain_end + '\n')
                        except:
                            print('%s资产错误！' % domain_tmp)
                            self.label_error.setText("error：%s资产错误！" % domain_tmp)
                key_domain.extend(list_tmp)
                lines = key_domain
                list_tmp = []
                list_tmp2 = []
                black_suffix = ['html', 'php', 'jsp', 'jspx', 'rar', 'zip', 'exe', 'pdf', 'doc', 'docx', 'avi', 'tmp',
                                'db', 'json', 'xls', 'xlsx', 'jpg', 'png', 'ico', 'img']
                pattern1 = '(?:http(?:s?)://)?[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}'
                pattern2 = '(?:http(?:s?)://)?(?:[\w|-]+\.)+[a-zA-Z]+'
                for line in lines:
                    if line.startswith('http://'):
                        line = line.replace('http://', '', 1)
                    elif line.startswith('https://'):
                        line = line.replace('https://', '', 1)
                    ip = re.search(pattern1, line)
                    domain = re.search(pattern2, line)
                    if domain:
                        if domain.group(0).split('.')[-1] not in black_suffix:
                            list_tmp.append(domain.group(0) + '\n')
                    elif ip:
                        list_tmp2.append(ip.group(0) + '\n')
                list_tmp = {}.fromkeys(list_tmp).keys()
                list_tmp2 = {}.fromkeys(list_tmp2).keys()
                self.plainTextEdit_output.setPlainText("".join(list_tmp) + "".join(list_tmp2))
                if self.current_step != len(self.operation_history) - 1:
                    self.operation_history = self.operation_history[:self.current_step + 1]
                    self.output_history = self.output_history[:self.current_step + 1]
                self.operation_history.append("提取根域名")
                self.output_history.append("".join(list_tmp) + "".join(list_tmp2))
                self.current_step += 1
                self.label_error.setText("")
            else:
                self.label_error.setText("error：输入内容为空")
        except Exception as e:
            print("Exception in main --> " + "func_get_root_domain", e)

    # fscan提取有效结果 4-1
    def func_get_fscan_plus(self):
        try:
            pass
            # list_tmp = []
            # with open(filename1, "r", encoding='utf-8') as f1:
            #     lines1 = f1.readlines()
            # with open(filename2, "r", encoding='utf-8') as f2:
            #     lines2 = f2.readlines()
            # for line in lines1:
            #     if line in lines2:
            #         list_tmp.append(line)
            # self.plainTextEdit_output.setPlainText("".join(list_tmp))
            # if self.current_step != len(self.operation_history) - 1:
            #     self.operation_history = self.operation_history[:self.current_step + 1]
            #     self.output_history = self.output_history[:self.current_step + 1]
            # self.operation_history.append("fscan提取有效结果")
            # self.output_history.append("".join(list_tmp))
            # self.current_step += 1
            # self.label_error.setText("")
        except Exception as e:
            print("Exception in main --> " + "func_get_fscan_plus", e)
            self.label_error.setText("error：读取错误！")

    # hackbrowser转换Cookie格式 4-2
    def func_convert_hb_cookie(self):
        try:
            pass
            # list_tmp = []
            # with open(filename1, "r", encoding='utf-8') as f1:
            #     lines1 = f1.readlines()
            # with open(filename2, "r", encoding='utf-8') as f2:
            #     lines2 = f2.readlines()
            # for line in lines1:
            #     if line in lines2:
            #         list_tmp.append(line)
            # self.plainTextEdit_output.setPlainText("".join(list_tmp))
            # if self.current_step != len(self.operation_history) - 1:
            #     self.operation_history = self.operation_history[:self.current_step + 1]
            #     self.output_history = self.output_history[:self.current_step + 1]
            # self.operation_history.append("hackbrowser转换Cookie格式")
            # self.output_history.append("".join(list_tmp))
            # self.current_step += 1
            # self.label_error.setText("")
        except Exception as e:
            print("Exception in main --> " + "func_convert_hb_cookie", e)
            self.label_error.setText("error：读取错误！")

    # 棱洞去除干扰行 4-3 // " 403 "、" 404 "、" [] "
    def func_remove_ehole_blank(self):
        try:
            pass
            # list_tmp = []
            # with open(filename1, "r", encoding='utf-8') as f1:
            #     lines1 = f1.readlines()
            # with open(filename2, "r", encoding='utf-8') as f2:
            #     lines2 = f2.readlines()
            # for line in lines1:
            #     if line in lines2:
            #         list_tmp.append(line)
            # self.plainTextEdit_output.setPlainText("".join(list_tmp))
            # if self.current_step != len(self.operation_history) - 1:
            #     self.operation_history = self.operation_history[:self.current_step + 1]
            #     self.output_history = self.output_history[:self.current_step + 1]
            # self.operation_history.append("棱洞去除干扰行")
            # self.output_history.append("".join(list_tmp))
            # self.current_step += 1
            # self.label_error.setText("")
        except Exception as e:
            print("Exception in main --> " + "func_remove_ehole_blank", e)
            self.label_error.setText("error：读取错误！")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建启动界面，支持png透明图片
    splash = QSplashScreen(QPixmap(':/flash.png'))
    splash.show()

    window = Window()
    # window.setWindowIcon(QIcon('resource/image/logo.png'))
    window.setWindowIcon(QIcon(':/logo.png'))
    window.resize(1150, 750)
    window.show()

    splash.finish(window)
    sys.exit(app.exec_())
