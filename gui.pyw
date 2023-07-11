from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget, QFileDialog, QMessageBox)

import sys
import os

import ia.inference as inference

import pandas as pd

class Ui_MainWindow(QWidget):
    def on_button_click(self):
        file_filter = 'Image File (*.png *.jpg *.jpeg)'
        response = QFileDialog.getOpenFileName(self, 'Abrir o arquivo', os.getcwd(), file_filter)
        dir = str(response).replace("('", "").replace("', 'Image File (*.png *.jpg *.jpeg)')", "")
        pixmap = QPixmap(dir)
        a = inference.inference(dir)
        output = 'Condição: {} | {} de probabilidade.'.format(inference.get_pred(a[0], a[1])[0], "{}%".format(inference.get_pred(a[0], a[1])[1]))
        self.label_3.setPixmap(pixmap)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setText(output)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prev = inference.Prev(path=dir, names=inference.get_classes(a[1]), probs=inference.get_preds(a[0]))
        prev.salvar()
        self.pushButton2.setVisible(True)
    


    '''*******************
    CLIQUE DO BOTÃO DE MAIS DETALHES QUE APARECE APÓS RODAR A PREVISÃO:
    *******************'''
    def on_button_click2(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Detalhes do resultado")

        ds = pd.read_csv("prev.csv", sep=";")
        ds = ds.tail(1)
        ds = ds.drop(columns=["path"])
        nome = ds["names"].values[0].replace("[", "").replace("]", "").replace("'","").replace(",","").split()
        prob = ds["probs"].values[0].replace("[", "").replace("]", "").replace(",","").split()

        prob = [float(i) for i in prob]
        combinado = list(zip(prob, nome))
        combinado_ordenado = sorted(combinado, reverse=True)

        prob_ordenado = [round(i[0], 4) for i in combinado_ordenado]
        nome_ordenado = [i[1] for i in combinado_ordenado]

        x= ""
        
        for i in range(len(nome)):
            if (prob_ordenado[i] <= 0.0001):
                prob_ordenado[i] = "\u22450"
            tempStr = "{}   \u2192   {}%".format(nome_ordenado[i], prob_ordenado[i])
            x += tempStr + "\n"

        dlg.setText(x)
        dlg.setFont(QFont("Arial", 12))
        dlg.exec()

    
    '''*******************
    CLIQUE DO BOTÃO DE LIMPAR O HISTÓRICO - JÁ ESTÁ PRONTO E FUNCIONANDO!:
    *******************'''
    def limparTodas(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Deletando o histórico")
        dlg.setText("Tem certeza de que deseja deletar o histórico?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            try:
                os.remove("prev.csv")
            except:
                print("Erro ao deletar o arquivo prev.csv (Não encontrado)")
        else:
            None


    '''*******************
    CLIQUE DO BOTÃO DE ABRIR O HISTÓRICO PELO MENU:
    ideia:
    - filtrar os dados com pandas e mostrá-los de uma forma visualmente agradável
    *******************'''
    def abrirPrev(self):
        pass


    '''*******************
    CLIQUE DO BOTÃO DE AJUDA PELO MENU (deixar por último):
    *******************'''
    def ajuda(self):
        pass


    '''*******************
    CLIQUE DO BOTÃO DE CRÉDITOS PELO MENU (deixar por último):
    *******************'''
    def creditos(self):
        pass


    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(902, 744)
        MainWindow.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 521, 71))
        font = QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(540, 30, 121, 41))
        self.pushButton.clicked.connect(self.on_button_click)

        self.pushButton2 = QPushButton(self.centralwidget)
        self.pushButton2.setObjectName(u"pushButton2")
        self.pushButton2.setFont(QFont("Arial", 12))
        self.pushButton2.setText(u"Mais detalhes")
        self.pushButton2.setVisible(False)
        self.pushButton2.setGeometry(QRect(385, 645, 131, 51))
        self.pushButton2.clicked.connect(self.on_button_click2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 570, 901, 61))
        font1 = QFont()
        font1.setPointSize(26)
        self.label_2.setFont(font1)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_2")
        self.label_3.setGeometry(QRect(0, 93, 901, 471))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 902, 22))
        self.help = QMenu(self.menubar)
        self.help.setObjectName(u"help")
        self.prev = QMenu(self.menubar)
        self.prev.setObjectName(u"prev")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.help.menuAction())
        self.menubar.addAction(self.prev.menuAction())
        self.prev.addSeparator()

        MainWindow.setWindowTitle(u"In\u00edcio")
        self.label.setText(u"Selecione o arquivo de imagem...")
        self.pushButton.setText(u"Selecionar")
        self.label_2.setText(u"")
        self.help.setTitle(u"Sobre")
        self.prev.setTitle(u"Previs\u00f5es anteriores")

        helpAct = QAction('Ajuda', self)
        credAct = QAction('Cr\u00e9ditos', self)

        self.help.addAction(helpAct)
        self.help.addAction(credAct)

        abrirAct = QAction('Abrir', self)
        delAct = QAction('Deletar', self)

        self.prev.addAction(abrirAct)
        self.prev.addAction(delAct)

        abrirAct.triggered.connect(self.abrirPrev)
        delAct.triggered.connect(self.limparTodas)
        helpAct.triggered.connect(self.ajuda)
        credAct.triggered.connect(self.creditos)
    # setupUi
    # retranslateUi



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
