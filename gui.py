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
    QWidget, QFileDialog, QFrame)
import sys
import os

import ia.inference as inference

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
        self.label_2.setText(QCoreApplication.translate("MainWindow", output, None))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prev = inference.Prev(path=dir, names=inference.get_classes(a[1]), probs=inference.get_preds(a[0]))
        prev.salvar()

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(902, 674)
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
        self.menuP_gina_inicial = QMenu(self.menubar)
        self.menuP_gina_inicial.setObjectName(u"menuP_gina_inicial")
        self.menuCr_ditos = QMenu(self.menubar)
        self.menuCr_ditos.setObjectName(u"menuCr_ditos")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuP_gina_inicial.menuAction())
        self.menubar.addAction(self.menuCr_ditos.menuAction())
        self.menuCr_ditos.addSeparator()


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"In\u00edcio", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Selecione o arquivo de imagem...", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Selecionar", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.menuP_gina_inicial.setTitle(QCoreApplication.translate("MainWindow", u"P\u00e1gina inicial", None))
        self.menuCr_ditos.setTitle(QCoreApplication.translate("MainWindow", u"Cr\u00e9ditos", None))
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

