from yt_dlp_gui import Ui_MainWindow

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# https://www.youtube.com/watch?v=XXPNpdaK9WA

class YourClassName(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        #self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)
        
    
    def func():
        print('hello')
    

if __name__ == '__main__':
    app = qtw.QApplication([])
    
    window = YourClassName()
    window.show()

    app.exec_()


