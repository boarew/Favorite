import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup as bs
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote_plus
from urllib.request import urlopen, Request, urlretrieve
import os
import re



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()

        #name search
        enter_btn = QPushButton("Search")
        self.namelabel = QLabel("Name:")
        self.line = QLineEdit(self)

        grid.addWidget(self.namelabel, 0, 0)
        grid.addWidget(self.line, 0, 1)
        grid.addWidget(enter_btn, 0 , 3)
        enter_btn.clicked.connect(self.enter)

        #exit_btn
        exit_btn = QPushButton("Exit")
        grid.addWidget(exit_btn, 3, 3)
        exit_btn.clicked.connect(QCoreApplication.instance().quit)
        #image layout

        self.img = QLabel()
        self.img.setFixedWidth(400)
        self.img.setFixedHeight(400)
        self.img.setAlignment(Qt.AlignCenter)
        self.img.setScaledContents(True)
        grid.addWidget(self.img, 2, 1)

        #check to save
        self.checksave = QCheckBox("Save", self)

        grid.addWidget(self.checksave, 2, 3)

        self.setLayout(grid)
        self.setGeometry(600, 750, 250, 250)
        self.setWindowTitle('입덕')

    def savepic(self, checksave, backup):
        if checksave.text() == "Save":
            if checksave.isChecked() == True:
                s =  backup + ".jpg"
                self.pixmap.save(s)
                checksave.setChecked(False)

    def enter(self):
        name = self.line.text()

        if name:
            self.backup = name
            self.searchimage(name)
            self.line.clear()
            self.checksave.stateChanged.connect(lambda:self.savepic(self.checksave, self.backup))

    def searchimage(self, name):

        url= 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='

        url = url + urllib.parse.quote_plus(name)

        html = urllib.request.urlopen(url).read()

        soup = bs(html, 'html.parser')
        #soup= soup.find("div",class_="thumb")
        img = soup.find("img")["src"]


        imgstr = str(img)

        if "&" in imgstr:
            imgstr=imgstr.split("&")[0]

        self.saveimg = urlopen(imgstr).read()
        self.pixmap = QPixmap()
        #self.pixmap.scaledToHeight(300)
        self.pixmap.loadFromData(self.saveimg)
        self.picture(self.pixmap)

        return

    def picture(self, pixmap):
        self.img.setPixmap(pixmap)
        return

def main():
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()
