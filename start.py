# @Time : 2020/5/16 21:04 
# -- coding: utf-8 --
# @Author : like

# @File : start.py.py

# @Description: xx
import os
import sys

from PyQt5.QtCore import QUrl, pyqtSignal, QObject
from PyQt5.QtGui import QDesktopServices, QTextCursor

from FreeForWenku import FreeDownloadWenku
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox

from mwin import Ui_MWin




# with open('Cookie.txt') as f:
#     headers['Cookie'] = f.read()

class MWin(QMainWindow, Ui_MWin):
    '''Lossless Music Box'''

    def __init__(self, parent=None):
        super(MWin, self).__init__(parent)
        self.setupUi(self)
        self.download_btn.clicked.connect(lambda: self.download(self.url_info.text()))
        self.open_download_fold_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('download')))
        sys.stdout = Stream(newText=self.onUpdateText)

    def download(self, url):
        type = self.type_Box.currentText()
        print('选择文件类型为:'+type)
        self.progressBar.setValue(0)
        try:
            self.fd = FreeDownloadWenku(url, type)
            #关联进度条
            self.fd.download_process_signal.connect(self.set_progressbar_value)
            self.fd.run()
        except:
            print('输入正确的url和文件类型')

    def onUpdateText(self, text):
        """Write console output to text widget.修改显示位置"""
        cursor = self.run_info.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.run_info.setTextCursor(cursor)
        self.run_info.ensureCursorVisible()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

        # 控制窗口显示在屏幕中心的方法

    def center(self):

        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点，QtGui,QDesktopWidget类提供了用户的桌面信息,包括屏幕大小
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 设置进度条
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "提示", "下载成功！")
            return


class Stream(QObject):
    """Redirects console output to text widget."""
    try:
        newText = pyqtSignal(str)
    except:
        print('Stream error')

    def write(self, text):
        self.newText.emit(str(text))


def main():
    app = QApplication(sys.argv)
    w = MWin()
    w.center()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        os.mkdir('downlaod')
    except Exception as e:
        print('目录已存在或无法创建')
    main()
