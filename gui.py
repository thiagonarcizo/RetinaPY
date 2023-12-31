# -*- coding: utf-8 -*-

from PySide6.QtCore import (QRect, Qt)
from PySide6.QtGui import (QAction, QColor, QFont, QIcon, QPalette, QPixmap)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu, QMenuBar, QPushButton, QStatusBar, QWidget, QFileDialog, QMessageBox, QVBoxLayout, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem)

import sys
import os
import subprocess
from datetime import datetime

import ia.inference as inference

import pandas as pd

import ctypes

import platform
if platform.system() == 'Windows':
    myappid = 'xyz.narcizo'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Verifica se o arquivo requirements.txt existe
if os.path.isfile('requirements.txt'):
    # Instala as dependências usando pip
    try:
        subprocess.Popen([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        os.remove('requirements.txt')
    except Exception as e:
        if platform.system() == 'Windows':
            os.system('cmd /c echo '+str(e)+' & PAUSE')
        else:
            os.system('echo '+str(e)+' && read -n 1 -r -p "Pressione qualquer tecla para continuar..."')
        sys.exit(1)

class Ui_MainWindow(QWidget):
    def on_button_click(self):
        file_filter = 'Image File (*.png *.jpg *.jpeg)'
        response = QFileDialog.getOpenFileName(self, 'Abrir o arquivo', os.getcwd(), file_filter)
        dir = str(response).replace("('", "").replace("', 'Image File (*.png *.jpg *.jpeg)')", "")
        try:
            pixmap = QPixmap(dir)
            a = inference.inference(dir)
            output = 'Condição: {} | {} de probabilidade.'.format(inference.get_pred(a[0], a[1])[0], "{}%".format(inference.get_pred(a[0], a[1])[1]))
            prev = inference.Prev(path=dir, names=inference.get_classes(a[1]), probs=inference.get_preds(a[0]))
            prev.salvar()
            self.pushButton2.setVisible(True)
            self.label_3.setPixmap(pixmap)
            self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except:
            output = ""
        self.label_2.setText(output)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    


    '''*******************
    CLIQUE DO BOTÃO DE MAIS DETALHES QUE APARECE APÓS RODAR A PREVISÃO:
    *******************'''
    def on_button_click2(self):
        dlg = QMessageBox(self)
        dlg.setWindowIcon(QIcon('icone.png'))
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
            x += tempStr + "\n\n"

        dlg.setText(x)
        dlg.setFont(QFont("Arial", 12))
        dlg.exec()

    
    '''*******************
    CLIQUE DO BOTÃO DE LIMPAR O HISTÓRICO - JÁ ESTÁ PRONTO E FUNCIONANDO!:
    *******************'''
    def limparTodas(self):
        dlg = QMessageBox(self)
        dlg.setWindowIcon(QIcon('icone.png'))
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
    *******************'''
    def abrirPrev(self):
        self.w = None
        MainWindow.show_new_window(self)


    '''*******************
    CLIQUE DO BOTÃO DE MOSTRAR O INÍICIO PELO MENU:
    *******************'''
    def inicioMenu(self):
        pass


    '''*******************
    CLIQUE DO BOTÃO DE AJUDA PELO MENU:
    *******************'''
    def ajuda(self):
        dlg = QMessageBox(self)
        dlg.setWindowIcon(QIcon('icone.png'))
        dlg.setWindowTitle("Ajuda")
        dlg.setTextFormat(Qt.TextFormat.RichText)
        dlg.setText('<p align=\"justify\">GUI amigável para predição de eventos adversos envolvendo análise de imagem de Tomografia de Coerência Óptica (OCT).<br>Utiliza o modelo pré-treinado Kermany, o qual dispõe de milhares de imagens de OCTs para treinamento da IA.</p><br><br>A Inteligência Artificial foi treinada para gerar 4 tipos de outputs:<br><b>- Diabetic Macular Edema (DME);<br>- Choroidal Neovascularization (CNV);<br>- Drusen;<br>- Normal.</b><br><br>* Informações do modelo: 288 camadas; 11.972.940 número total de weights; eficácia de 99,8%<br><br>PS: Toda probabilidade que for igual a 100% é arredondada!')
        dlg.setFont(QFont("Arial", 16))
        dlg.exec()


    '''*******************
    CLIQUE DO BOTÃO DE CRÉDITOS PELO MENU:
    *******************'''
    def creditos(self):
        dlg = QMessageBox(self)
        dlg.setWindowIcon(QIcon('icone.png'))
        dlg.setWindowTitle("Cr\u00e9ditos")
        dlg.setTextFormat(Qt.TextFormat.RichText)
        dlg.setText('<p align=\"justify\">Idealizado e feito por <a href=\"https://github.com/thiagonarcizo/\">Thiago Narcizo</a> e por <a href=\"https://github.com/mathfaria\">Matheus Faria</a><br>com base no modelo de IA pré-treinada de OCT de <a href=\"https://www.sciencedirect.com/science/article/pii/S0092867418301545\">Kermany</a>.</p><br><br><a href=\"https://github.com/thiagonarcizo/RetinaPY\">Link do projeto no GitHub</a><br><br>Versão: 1.0.1')
        dlg.setFont(QFont("Arial", 16))
        dlg.exec()



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

        self.menubar.addAction(self.prev.menuAction())
        self.menubar.addAction(self.help.menuAction())
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

class Ui_PrevWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.old_key_state = Qt.NoModifier
        self.setWindowIcon(QIcon('icone.png'))
        self.resize(702, 544)
        self.setFixedSize(self.size())
        self.setWindowFlags(self.windowFlags() & Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowTitle('Previs\u00f5es anteriores')
        if os.path.isfile('prev.csv'):
            self.ds = pd.read_csv('prev.csv', sep=';')
            self.ds = self.ds[::-1]
            self.rows = len(self.ds.index)
            self.columns = len(self.ds.columns)
            self.table = QTableWidget()
            self.table.setRowCount(self.rows)
            self.table.setColumnCount(self.columns)
            self.table.setHorizontalHeaderLabels(["Imagem", "Condi\u00e7\u00e3o", "Probabilidade (%)", "Data"])

            self.centralwidget = QWidget(self)

            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for i in range(self.rows):
                self.table.setRowHeight(i, 100)
                font = QFont()
                font.setPointSize(12)
                label = QLabel()
                if os.path.isfile(self.ds.iloc[i, 0]):
                    pixmap = QPixmap(self.ds.iloc[i, 0])
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                else:
                    label.setText('Imagem não encontrada!\n\nLocal anterior:\n'+'('+str(self.ds.iloc[i, 0])+')')
                self.table.setCellWidget(i, 0, label)

                item1 = QTableWidgetItem(self.ds.iloc[i, 1].replace("[", "").replace("]", "").replace("'","").replace(",","").replace(" ","\n"))
                item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item1.setFont(font)
                self.table.setItem(i, 1, item1)

                item2 = QTableWidgetItem(str(self.ds.iloc[i, 2].replace("[", "").replace("]", "").replace("'","").replace(",","").replace(" ","\n")))
                item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item2.setFont(font)
                self.table.setItem(i, 2, item2)

                data = datetime.strptime(self.ds.iloc[i, 3], "%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y às %H:%M")
                item3 = QTableWidgetItem(data)
                item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item3.setFont(font)
                self.table.setItem(i, 3, item3)

            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.vBox = QVBoxLayout(self.centralwidget)
            self.vBox.addWidget(self.table)
            self.vBox.setAlignment(Qt.AlignCenter)
            self.setLayout(self.vBox)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and event.modifiers() & Qt.ControlModifier:
            self.close()



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui_prev = Ui_PrevWindow()
        self.setFixedSize(self.size())

        self.old_key_state = Qt.NoModifier

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and event.modifiers() & Qt.ControlModifier:
            self.close()
        elif (event.key() == 16777220) or (event.key() == 43):
            Ui_MainWindow.on_button_click(self)
        elif event.key() == Qt.Key_H and event.modifiers() & Qt.ControlModifier:
            Ui_MainWindow.abrirPrev(self)


    def show_new_window(self):
        if os.path.isfile('prev.csv'):
            if self.w is None:
                self.w = Ui_PrevWindow()
            self.w.show()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowIcon(QIcon('icone.png'))
            dlg.setWindowTitle("Erro!")
            dlg.setTextFormat(Qt.TextFormat.RichText)
            dlg.setText('<p>O arquivo de histórico não foi encontrado.</p>')
            dlg.setFont(QFont("Arial", 20))
            dlg.exec()


    def get_darkModePalette(app=None):
        
        darkPalette = app.palette()
        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.WindowText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
        darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        darkPalette.setColor(QPalette.Text, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor( 127, 127, 127))
        darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
        darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ButtonText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        darkPalette.setColor(QPalette.BrightText, Qt.red)
        darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        darkPalette.setColor(QPalette.HighlightedText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127),)
        
        return darkPalette

if __name__ == "__main__":
    app = QApplication(sys.argv + ['-platform'])
    app.setStyle('Fusion')
    #app.setPalette(MainWindow.get_darkModePalette(app))

    window = MainWindow()
    app.setWindowIcon(QIcon('icone.ico'))
    window.show()

    sys.exit(app.exec())
