from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import sys
from OYSform import Ui_MainWindow

students=[
    {'isim':'Eren', 'Yaş':'20', 'notu':81, 'Durumu':'', 'Karesi':''},
    ]

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStudents(students)
        self.ui.btn_ekle.clicked.connect(self.addStudent)
        self.ui.btn_guncelle.clicked.connect(self.updateTbl)
        self.ui.btn_arama.clicked.connect(self.searchTbl)

    def searchTbl(self):
        index=self.ui.txt_arama.text().lower().strip()
        searches=[student for student in students if index == student['isim'].lower()]
        self.loadStudents(searches)
                
    def updateTbl(self):
        item = self.ui.cb_gecenler.isChecked()
        if item==True:
            gecenler=[student for student in students if int(student['notu'])>=50]
            self.loadStudents(gecenler)
            
        else:
            self.loadStudents(students)
            
    def addStudent(self):
        name=self.ui.txt_isim.text()
        age=self.ui.txt_yas.text()
        score=self.ui.txt_not.text()
        for student in students:
            if name==student['isim']: 
                self.showError()
                return
        students.append({'isim':name, 'Yaş':age, 'notu':score, 'Durumu':'', 'Karesi':''})
        self.loadStudents(students) 

    def showError(self):
        msg=QMessageBox()
        msg.setWindowTitle("Hata")
        msg.setText('Öğrenci zaten kayıtlı.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def loadStudents(self,liste):
        self.ui.tbl_liste.setRowCount(len(liste))
        self.ui.tbl_liste.setColumnWidth(0,80)
        self.ui.tbl_liste.setColumnWidth(1,10)
        self.ui.tbl_liste.setColumnWidth(2,10)
        self.ui.tbl_liste.setColumnWidth(3,70)
        self.ui.tbl_liste.setColumnWidth(4,60)

        rowIndex = 0
        for student in liste:
            if int(student['notu'])>=50: durum='Geçti'
            else:durum='Kaldı'
            self.ui.tbl_liste.setItem(rowIndex,0,QTableWidgetItem(student['isim']))
            self.ui.tbl_liste.setItem(rowIndex,1,QTableWidgetItem(student['Yaş']))
            self.ui.tbl_liste.setItem(rowIndex,2,QTableWidgetItem(str(student['notu'])))
            self.ui.tbl_liste.setItem(rowIndex,3,QTableWidgetItem(durum))
            self.ui.tbl_liste.setItem(rowIndex,4,QTableWidgetItem(str(int(student['notu'])**2)))
            rowIndex += 1
             
def app():
    app=QtWidgets.QApplication(sys.argv)
    win=App()
    win.show()
    sys.exit(app.exec_())

app()
