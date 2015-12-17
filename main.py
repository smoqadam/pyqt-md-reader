import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import os.path
import markdown
import mimetypes


class Reader(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(500, 500)
        self.web_view = WebView(self)
        self.setCentralWidget(self.web_view)

        self.statusBar().showMessage('Ready')
        self.web_view.loadFinished.connect(self._load_finished)


        self.createMenu()

    
    def _load_finished(self):
        frame = self.web_view.page().mainFrame()
        self.web_view.page().setViewportSize(frame.contentsSize())
        self.resize(frame.contentsSize())
        html_data = frame.toHtml()


    def createMenu(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        openAction = QAction(QIcon('open.png'),'&Open',self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Markdown file')
        openAction.triggered.connect(self.openNewFile)
        
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        aboutAction = QAction(QIcon(''),'&About',self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.showAboutDialog)
        aboutMenu = menubar.addMenu('&About')
        aboutMenu.addAction(aboutAction)
        

    def showAboutDialog(self):
        self.statusBar().showMessage('source code: github.com/smoqadam/pyqt-md-reader')

    def openNewFile(self):
        self.statusBar().showMessage('OPEN')
        try :
            fname = QFileDialog.getOpenFileName(self,'open file','','All Text Files (*.md *.markdown *.txt *.*)',None,QFileDialog.DontUseNativeDialog)      
            self.web_view.showMarkdown(fname)
        except UnicodeDecodeError :
            self.statusBar().showMessage('Please select only text files')
        except IOError:
            self.statusBar().showMessage('File open canceled!')


        
class WebView(QWebView):
    def __init__(self, parent=None):
        super(WebView, self).__init__(parent)
        self.main = parent

    def dragEnterEvent(self, event):
        u = event.mimeData().urls()
        for url in u:
            self.filePath = os.path.abspath(url.toLocalFile())

            ext = self.filePath.split('.')[-1]
            if ext in ['txt','md','markdown']:
                event.accept()
            else :
                event.ignore()


    def dropEvent(self, event):
        event.accept()
        self.showMarkdown(self.filePath)

    def contextMenuEvent(self,e):
        'do nothing on right click'

    def showMarkdown(self,filePath):
        markdown_file = open(filePath)
        file_content = markdown_file.read()
        self.setHtml(markdown.markdown(file_content))
        self.main.statusBar().showMessage(filePath)


    
def main():
    qtapp = QApplication(sys.argv)
    reader = Reader()
    reader.web_view.load(QUrl('blank'))
    reader.show()
    qtapp.exec_()


if __name__ == '__main__':
    main()
