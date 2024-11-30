import sys
from getai import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFrame, QLabel, QScrollArea


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('聊天界面')
        self.setGeometry(100, 100, 700, 400)  # 设置窗口宽度为700，高度为400

        self.setFixedSize(700, 400)  # 设置窗口的固定大小
        self.init_ui()

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout()

        # 创建一个背景框（容器），用于显示消息
        self.chat_container = QVBoxLayout()

        # 用于显示消息的区域
        chat_area = QFrame(self)
        chat_area.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 10px;")
        chat_area.setLayout(self.chat_container)

        # 输入框和按钮的布局
        input_layout = QHBoxLayout()

        # 创建圆角的输入框
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("请输入消息...")
        self.text_input.setFont(QFont('Arial', 10))

        # 设置输入框的圆角
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 5px;
                background-color: #ffffff;
            }
        """)

        # 限制输入框的最大行数（3行）
        self.text_input.setMaximumHeight(60)
        self.text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 发送按钮
        self.send_button = QPushButton('Send', self)
        self.send_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        # 设置输入框和发送按钮的布局，确保它们水平居中
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_button)

        # 创建一个背景框（容器），用于输入框和按钮
        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")  # 背景色和圆角
        background_frame.setFrameShape(QFrame.StyledPanel)
        background_frame.setLayout(input_layout)

        # 设置输入框和发送按钮的比例，使它们居中显示
        background_frame.setFixedHeight(80)
        input_layout.setStretch(0, 7)  # 设置输入框的比例
        input_layout.setStretch(1, 3)  # 设置发送按钮的比例

        # 将消息区域和输入框的背景框添加到主布局
        main_layout.addWidget(chat_area)
        main_layout.addWidget(background_frame)

        # 设置主布局
        self.setLayout(main_layout)

        # 创建一个滚动区域，并将聊天容器放入其中
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(chat_area)

        # 将滚动区域添加到主布局
        main_layout.addWidget(scroll_area)

    def send_message(self):
        text = self.text_input.toPlainText().strip()

        # 创建消息标签，背景色与发送按钮相同
        message = QLabel(text, self)
        # 用户没有输入时，不生成消息
        if text == "":
            return

        # 创建消息标签，背景色与发送按钮相同

        message.setWordWrap(True)  # 自动换行
        message.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 右对齐并垂直居中

        # 设置消息框的样式，背景色与发送按钮相同
        message.setStyleSheet("""
            QLabel {
                background-color: #4caf50  ;  # 使用与按钮相同的颜色
                border-radius: 10px;
                padding: 10px;
                color: green;
                margin-bottom: 10px;
                max-width: 300px;  # 限制消息框的最大宽度
            }
        """)

        # 将消息添加到聊天区域
        self.chat_container.addWidget(message)
        self.text_input.clear()  # 清空输入框
        aihui = getaireturn(text)
        self.aisend(aihui)

    def aisend(self, text):
        # 创建消息标签，背景色与发送按钮相同
        message = QLabel(text, self)
        message.setWordWrap(True)  # 自动换行
        message.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 右对齐并垂直居中

        # 设置消息框的样式，背景色与发送按钮相同
        message.setStyleSheet("""
                    QLabel {
                        background-color: #4CAF50;  # 使用与按钮相同的颜色
                        border-radius: 10px;
                        padding: 10px;
                        color: white;
                        margin-bottom: 10px;
                        max-width: 300px;  # 限制消息框的最大宽度
                    }
                """)

        # 将消息添加到聊天区域
        self.chat_container.addWidget(message)
        self.text_input.clear()  # 清空输入框


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
