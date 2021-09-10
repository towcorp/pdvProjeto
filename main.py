from PyQt5 import  uic,QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout

import mysql.connector
from reportlab.pdfgen import canvas

app=QtWidgets.QApplication([])
vendas=uic.loadUi("vendas.ui")
vendas.vendas = QTabWidget()

#=========================CONECTAR BANCO DE DADOS============================================

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123",
    database="estoque_produtos"
)

#============================================================================================

def venderProdutos():
    print("funcionando")
    linha1 = vendas.cpCodigoVenda.text()
    print(linha1)
''


def cadastrarProduto():

    linha1 = vendas.cpCodigoCadastro.text()
    linha2 = vendas.cpProdutoCadastro.text()
    linha3 = vendas.cpCategoriaCadastro.text()
    linha4 = vendas.cpEstoqueMinimoCadastro.text()
    linha5 = vendas.cpQuantidadeCadastro.text()
    linha6 = vendas.cpPrecoCadastro.text()
    
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,produto,categoria,estoque_minimo,quantidade,preco) VALUES(%s,%s,%s,%s,%s,%s)" 
    dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5),str(linha6))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    
    vendas.cpCodigoCadastro.setText("")
    vendas.cpProdutoCadastro.setText("")
    vendas.cpCategoriaCadastro.setText("")
    vendas.cpEstoqueMinimoCadastro.setText("")
    vendas.cpQuantidadeCadastro.setText("")
    vendas.cpPrecoCadastro.setText("")


def consultarEstoque():

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)
    vendas.tableWidget.setRowCount(len(dados_lidos))
    vendas.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            vendas.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



    categoria = ""
    if vendas.rbEstoqueMinimoEstoque.isChecked():
        categoria = "estoque minimo"
    elif vendas.rbSemEstoqueEstoque.isChecked():
        categoria = "sem estoque"
    else:
        categoria = "categoria"
    


vendas.btBuscarProdutoVenda.clicked.connect(venderProdutos)
vendas.btCadastrarCadastro.clicked.connect(cadastrarProduto)
vendas.btPesquisarEstoque.clicked.connect(consultarEstoque)



















#===============================RODAR APLICAÇÃO =============================================

vendas.show()
app.exec()
