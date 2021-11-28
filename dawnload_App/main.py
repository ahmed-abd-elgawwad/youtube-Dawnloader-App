# importing the qt and the related libyraries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import os
from os import path
import urllib.request
import pafy
import humanize
from pytube import Playlist
from pytube import YouTube
from threading import Thread
import urllib
import urllib3
import time


def enable():
    os.system("netsh interface set interface 'Wifi' enabled")

def disable():
    os.system("netsh interface set interface 'Wifi' disabled")
FORM_CLASS,_ =loadUiType(path.join(path.dirname(__file__),"main.ui"))
class MainApp(QMainWindow,FORM_CLASS):
    def __init__(self,parent =None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui_settings()
        self.buttons()
    # handling the ui settings
    def ui_settings(self):
        self.setFixedSize(770,416)
        self.setWindowTitle("Dawnloader")
    # hindeling button and connecting them
    def buttons(self):
        self.pushButton_2.clicked.connect(self.Hundle_browse1)
        self.pushButton_3.clicked.connect(self.Hundle_browse2)
        self.dawnload.clicked.connect(self.Dawnload)
        self.dawnload_2.clicked.connect(self.Dawnload_youtube_video)
        self.pushButton_5.clicked.connect(self.get)
        self.pushButton_4.clicked.connect(self.Hundle_browse3)
        self.pushButton_6.clicked.connect(self.Search_list)
        self.dawnload_3.clicked.connect(self.Dawnload_list)

    def Hundel_progressBar(self,block_number, block_size, totalsize):
        read = block_number * block_size
        if totalsize > 0:
            percent = read *100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()

    def Dawnload(self):
        url = self.lineEdit.text()
        location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url,location,self.Hundel_progressBar)
        except:
            QMessageBox.warning(self,"Dawload error"," there is something wrong in the dawnloading")
        else:
            QMessageBox.information(self,"Compeleted","the dawnload is compelete")
            self.lineEdit.setText("")
            self.progressBar.setValue(0)
    def Hundle_browse1(self):
        if self.lineEdit.text() == "":
            QMessageBox.warning(self, "Error", "Put the url first,idiot")
        else:
            save_location = QFileDialog.getExistingDirectory(self, "select the directory")
            self.lineEdit_2.setText(save_location)

    def Hundle_browse2(self):
        if self.lineEdit_3.text() == "":
            QMessageBox.warning(self, "Error", "Put the url first,idiot")
        else:
            save_location = QFileDialog.getExistingDirectory(self, "select the directory")
            save_location = str(save_location)
            self.lineEdit_4.setText(save_location)

    def Hundle_browse3(self):
        if self.lineEdit_5.text() == "":
            QMessageBox.warning(self,"Error","Put the url first,idiot")
        else:
            save_location = QFileDialog.getExistingDirectory(self, "select the directory")
            save_location = str(save_location)
            self.lineEdit_6.setText(save_location)
# get streams is to handle the [ search button of the video ] and get the video informations

    def get(self):
        try:
            if self.lineEdit_3.text() =="":
                QMessageBox.warning(self,"Error","Put the link first.")
            else:
                url = self.lineEdit_3.text()
                self.thread = QThread(parent=self)
                # Step 3: Create a worker object
                self.worker = Worker(url=url)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.worker.compo.connect(self.comboBox.addItem)
                # Step 6: Start the thread
                self.thread.start()

                # Final resets
                self.pushButton_5.setEnabled(False)
                self.thread.finished.connect(lambda: self.pushButton_5.setEnabled(True))
        except:
            QMessageBox.warning(self, "error", "wrong url or internet connection error")
# handle the [download button] of the video
    def Dawnload_youtube_video(self):
        try:
            if self.lineEdit_4.text() =="" :
                QMessageBox.warning(self, "Note", "Choose the location first,idiot.")
            elif self.comboBox.currentText == None:
                QMessageBox.warning(self, "Note", "Choose the type first.")
            else:
                url = self.lineEdit_3.text()
                save_location = self.lineEdit_4.text()
                video = pafy.new(url)
                streams = video.allstreams
                index = self.comboBox.currentIndex()
                os.chdir(save_location)
                if os.path.isfile(f"{video.title}.{streams[index].extension}"):
                    QMessageBox.warning(self, "Warning", "The file already exist")
                    self.comboBox.clear()
                else:
                    dawnload= streams[index].download(filepath = save_location,callback=self.Video_progress)
                    QMessageBox.information(self, "Success", "The dawnload is compelete")
                    self.comboBox.clear()
                    self.progressBar_2.setValue(0)
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
        except:
            QMessageBox.warning(self, "Error","Internet connections error")
            self.progressBar_2.setValue(0)
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.comboBox.clear()
    def Video_progress(self,total_size,downlaoded_size,ratio,dawnload_rate,EtA):
        percent = ratio *100
        self.progressBar_2.setValue(percent)
        self.label_10.setText(str(int(dawnload_rate))+" kb/s")
        self.label_11.setText(str(EtA)+"s")
        QApplication.processEvents()
    def success_dawnload(self):
       pass

    def Dawnload_list(self):
        try:
            index = 0
            if self.lineEdit_6.text() =="":
                QMessageBox.warning(self,"Note","Choose the location first,idiot.")
            elif self.lcdNumber.value() == 0:
                QMessageBox.warning(self, "Note", "Search first for the link,click Search button.")
            else:
                url = self.lineEdit_5.text()
                save_location = self.lineEdit_6.text()
                p = Playlist(url)
                urls = p.video_urls
                os.chdir(save_location)
                i=1


                for url in urls:
                    video = pafy.new(url)
                    dawnload =video.getbest().download(filepath=save_location, callback=self.Video_progress2)
                    self.lcdNumber_2.display(i)
                    i+=1
                    index+=1
                QMessageBox.information(self, "success", "Downloading the playlist was successful")
                self.progressBar_3.setValue(0)
                self.lineEdit_5.setText("")
                self.lineEdit_6.setText("")
        except:
            # QMessageBox.warning(self,"Error","Something went wrong.maybe an internet connection err")
            # urls = urls[index::]
            disable()
            time.sleep(5)
            enable()
            self.Dawnload_list()

    # [ 2 ] the progress of the download
    def Video_progress2(self,total_size,downlaoded_size,ratio,dawnload_rate,EtA):
        percent = ratio *100
        self.progressBar_3.setValue(percent)
        self.label_14.setText(str(int(dawnload_rate))+" kb/s")
        self.label_15.setText(str(EtA)+"s")
        QApplication.processEvents()
    # [ 3 ] the search button to get the information
    def Search_list(self):
        try:
            url = self.lineEdit_5.text()
            p = Playlist(url)
            self.lcdNumber.display(len(p.video_urls))
            QApplication.processEvents()

        except:
            QMessageBox.warning(self, "Error", "Wrong url or internet connection error.Please, put a video url")
# threading  to get the streams fo the video
class Worker(QObject):
    finished = pyqtSignal()
    compo = pyqtSignal(str)
    def __init__(self,url):
        super(Worker, self).__init__()
        self.url=url
    def run(self):
        """Long-running task."""
        video = pafy.new(self.url)
        for i in video.allstreams:
            size = humanize.naturalsize(i.get_filesize())
            data = f"{str(i.mediatype).title()} || {i.extension} | {i.quality} | {size}"
            self.compo.emit(data)
        self.finished.emit()
# the threading for the progressbar
class progress_bar_threading(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    label1 = pyqtSignal(str)
    label2 = pyqtSignal(str)
    def __init__(self, ratio, rate, time):
        super(progress_bar_threading, self).__init__()
        self.ratio = ratio
        self.rate = rate
        self.time =  time
    def run(self):
        while self.ratio <= 1:
            percent = (int(self.ratio)) * 100
            self.progress.emit(percent)
            self.label1.emit(str(self.rate))
            self.label2.emit(str(self.time))
        self.finished.emit()

# start looping the programs
def main():
    app =QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__=="__main__":
    main()
    input()
