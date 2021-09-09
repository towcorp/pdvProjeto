from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

app=QtWidgets.QApplication([])
vendas=uic.loadUi("vendas.ui")

vendas.show()
app.exec()
