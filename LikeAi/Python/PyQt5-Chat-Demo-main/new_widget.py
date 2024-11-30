from PyQt5 import QtCore, QtWidgets

class Set_question:
    def set_return(self, ico, text, dir):  # 头像，文本，方向
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget.setLayoutDirection(dir)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(ico)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setStyleSheet("padding:10px;\n"
                                       "background-color: rgba(71,121,214,20);\n"
                                       "font: 16pt \"黑体\";")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText(text)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.widget)

        # 新增：使用 QTimer 实现逐字输出效果
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_text)
        self.timer.start(100)
        self.text_index = 0

    def show_text(self):
        if self.text_index < len(self.textBrowser.toPlainText()):
            self.textBrowser.setText(self.textBrowser.toPlainText()[:self.text_index + 1])
            self.text_index += 1
        else:
            self.timer.stop()
