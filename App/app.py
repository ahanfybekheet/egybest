import sys
import webbrowser
import requests
from main_window import Ui_MainWindow
from choose_quality import Ui_Dialog
from about import Ui_Form
from progressBar import Ui_Progress


from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow
)
from PyQt5.QtCore import (
    QObject, QThread, pyqtSignal
)
from egybest import (
    Search,download
)

class Worker(QObject):

    finished = pyqtSignal() #Initialize signal To use it as thing to tell thread that worker has finished
    setProgressValue = pyqtSignal(str) #Initialize signal to use it as thing that send the value of label text

    def __init__(self,movie_link:str = '',quality:str = ''):
        ''' :movie_link: To use it in Movie instance 
            :quality: To use it in Movie instance '''
        super().__init__()
        self.movie_link = movie_link #To be able to call in run function
        self.quality = quality       #To be able to call in run function

    def run(self):
        '''get source of the movie'''
        global data #Make it global to use it in run2
        data = download(self.movie_link,self.quality) 
        self.finished.emit()

        

    def run2(self):
        '''download the movie with request library'''
        r= requests.get(data[0],stream=True)
        f_size = 0
        with open(f'{data[1]}.mp4', 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk)
                    f_size += 1
                    self.setProgressValue.emit(f'{f_size} MB')
        self.finished.emit()



class Window(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        '''initialize Connects And Slots'''

        self.pushButton.clicked.connect(self.showResult) 
        self.pushButton_2.clicked.connect(self.download) 
        self.pushButton_5.clicked.connect(self.close) 
        self.actionExit.triggered.connect(self.close) 
        self.actionAbout.triggered.connect(self.about) 
        self.pushButton_3.clicked.connect(self.about)
        self.actionHelp.triggered.connect(self.help)

    def showResult(self):
        '''add Films To comboBox'''
        self.search = Search(self.lineEdit.text())
        for i in range(len(self.search.results_title)):
            self.comboBox.addItem(self.search.results_title[i].text)
        
    def download(self):
        dialog = Quality()
        dialog.exec()
        movie_link = self.search.get_result_link(self.comboBox.currentIndex())  
        self.thread = QThread() #make thread instance
        self.worker = Worker(movie_link,dialog.quality) #make worker instance
        self.worker.moveToThread(self.thread) #move worker to work on thread instace .. not main thread(default thread)
        self.thread.started.connect(self.worker.run) #when thread start call worker run function
        self.worker.finished.connect(self.worker.deleteLater) #when worker finished signal called .. delete worker from memory
        self.worker.finished.connect(self.progress) #when worker finished signal called .. delete worker from memory
        self.worker.finished.connect(self.thread.quit) #when worker finished signal called .. end the thread
        self.thread.finished.connect(self.thread.deleteLater) #when thread finished signal called .. delete thread from memory
        self.thread.start()



    def about(self):
        self.dialog = About()
        self.dialog.exec()

    def help(self):
        webbrowser.open('https://www.github.com/ahanfybekheet/egybest')

    def progress(self):
    
        self.dialog = Progress()
        self.dialog.exec()

class Quality(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.ok)
        self.pushButton_2.clicked.connect(self.close)

    def ok(self):
        self.quality = self.comboBox.currentText()
        self.close()

class About(QDialog,Ui_Form):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.close)

class Progress(QDialog,Ui_Progress):
    def __init__(self) :
        super().__init__()
        self.ui = Ui_Dialog()
        self.setupUi(self)
        self.label_4.setHidden(True)
        self.label.setText(data[1])
        self.connectSignalsSlots()
        self.show_progress()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.close)

        
    def show_progress(self):
    
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run2)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.enable_text)
        self.worker.setProgressValue.connect(self.label_3.setText)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def enable_text(self):
        self.label_4.setHidden(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())