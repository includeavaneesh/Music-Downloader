import os 
import sys
import pafy

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *  
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

from youtube_search import YoutubeSearch

class main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


        self.setWindowIcon(QtGui.QIcon('./images/icon.ico.png'))
        self.setMinimumSize(QSize(700, 700))    
        self.setWindowTitle("Lost in Music") 
        self.setStyleSheet("background-color: #2A2D32; color: #99AAB5;text-align: center")
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)
        
        self.Song_Name = QLabel(self)
        self.Song_Name.setText("Song Name")
        self.Song_Name.setFont(QFont('Arial', 12))
        self.Song_Name.move(30, 150)

        self.Song_Name_input = QLineEdit(self)
        self.Song_Name_input.move(170, 150)
        self.Song_Name_input.resize(500, 32)
        self.Song_Name_input.setStyleSheet("background-color: white; border-radius: 10px; font-size: 15px; color: #2A2D32 ")
        

        self.url = QLabel(self)
        self.url.setText("Song URL")
        self.url.setFont(QFont('Arial', 12))
        self.url.move(30, 250)

        self.url_input = QLineEdit(self)
        self.url_input.move(170, 250)
        self.url_input.resize(500, 32)
        self.url_input.setStyleSheet("background-color: white; border-radius: 10px; font-size: 15px; color: #2A2D32 ")

        pybutton = QPushButton('Find and Download',self)
        pybutton.resize(300,40)
        pybutton.move(200,350)
        pybutton.clicked.connect(self.find_download)
        pybutton.setStyleSheet("""
            QPushButton{
                border-radius : 20px; 
                border : 0px solid black; 
                background: #7289DA; 
                color: 'white'; 
                font-size: 20px;
            }
        
        """)

    def find_download(self):
        print("Started finding....")

        if(self.Song_Name_input.text() != ""):
            results = YoutubeSearch(self.Song_Name_input.text(), max_results=1).to_dict()
            print(results[0]['url_suffix'])
            url = "https://www.youtube.com" + results[0]['url_suffix']
        
        # youtube
        elif(self.url_input.text() != ""):
            url = self.url_input.text()
            
        video = pafy.new(url)  
        audiostreams = video.audiostreams
        to_download = 0
        max_quality = 0
        best_quality_m4a = 0

        for i in audiostreams:
            if(i.extension == "m4a"):
                if(float(i.bitrate[:-1])*1000 > max_quality):
                    index = best_quality_m4a
                    print(i.bitrate, i.extension, i.get_filesize())
            best_quality_m4a += 1

        
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        print(folderpath)
        
        if(folderpath != ""):
            os.chdir(folderpath)
        audiostreams[index].download()

        # song name


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = main()
    mainWin.show()
    sys.exit( app.exec_() )
