from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtWidgets import QFileDialog, QDialog
from definitions import ROOT_DIR
from PyQt5 import QtCore

def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    mainWindow.setGeometry(200, 200, 300, 300)
    mainWindow.setWindowTitle("Window Title")
    #mainWindow.resize(300, 300)

    label = QtWidgets.QLabel(mainWindow)
    label.setText("Label Text")
    label.move(50, 50)

    mainWindow.show()
    sys.exit(app.exec_())

def FileDialog(directory='', forOpen=True, fmt='', isFolder=False):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)

    # ARE WE TALKING ABOUT FILES OR FOLDERS
    if isFolder:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
    else:
        dialog.setFileMode(QFileDialog.AnyFile)
    # OPENING OR SAVING
    dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)

    # SET FORMAT, IF SPECIFIED
    if fmt != '' and isFolder is False:
        dialog.setDefaultSuffix(fmt)
        dialog.setNameFilters([f'{fmt} (*.{fmt})'])

    # SET THE STARTING DIRECTORY
    if directory != '':
        dialog.setDirectory(str(directory))
    else:
        dialog.setDirectory(str(ROOT_DIR))

dialog = QFileDialog()
foo_dir = dialog.getExistingDirectory(self, 'Select an awesome directory')
print(foo_dir)

main()