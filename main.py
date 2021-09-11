from PyQt5 import  uic,QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QMessageBox

import mysql.connector
from reportlab.pdfgen import canvas

app=QtWidgets.QApplication([])
vendas=uic.loadUi("vendas.ui")
tela_editar=uic.loadUi('menu_editar.ui')
vendas.vendas = QTabWidget()

#=========================CONECTAR BANCO DE DADOS============================================
numero_id = 0

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

    
    if vendas.rbEstoqueMinimoEstoque.isChecked():
        

        comando_SQL = "SELECT * FROM produtos WHERE quantidade <= estoque_minimo ORDER BY quantidade"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
       
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    elif vendas.rbCategoriaEstoque.isChecked():
     

        comando_SQL = "SELECT * FROM produtos GROUP BY codigo ORDER BY categoria"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
        
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    else:   
        comando_SQL = "SELECT * FROM produtos"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
       
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    



    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            vendas.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def atualizar_tela():
    vendas.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    vendas.tableWidget.setRowCount(len(dados_lidos))
    vendas.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
           vendas.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 


def editar_dados():
    global numero_id

    linha = vendas.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE codigo="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    tela_editar.leCodigo.setText(str(produto[0][0]))
    tela_editar.leProduto.setText(str(produto[0][1]))
    tela_editar.leCategoria.setText(str(produto[0][2]))
    tela_editar.leEstoqueMin.setText(str(produto[0][3]))
    tela_editar.leQuantidade.setText(str(produto[0][4]))
    tela_editar.lePreco.setText(str(produto[0][5]))
    

    numero_id = valor_id


def salvar_valor_editado():
    global numero_id

    # ler dados do lineEdit
    codigo = tela_editar.leCodigo.text()
    produto = tela_editar.leProduto.text()
    categoria = tela_editar.leCategoria.text()
    estoque_minimo = tela_editar.leEstoqueMin.text()
    quantidade = tela_editar.leQuantidade.text()
    preco = tela_editar.lePreco.text()

    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', produto = '{}', categoria = '{}', estoque_minimo ='{}', quantidade ='{}', preco ='{}' WHERE codigo = {}".format(codigo,produto,categoria,estoque_minimo,quantidade,preco, numero_id))
    banco.commit()
    #atualizar as janelas
    tela_editar.close()
    vendas.close()
    atualizar_tela()



def excluir_dados():

    cursor = banco.cursor()

    if vendas.rbEstoqueMinimoEstoque.isChecked():
        

        comando_SQL = "SELECT * FROM produtos WHERE quantidade <= estoque_minimo ORDER BY quantidade"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
       
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    elif vendas.rbCategoriaEstoque.isChecked():
     

        comando_SQL = "SELECT * FROM produtos GROUP BY codigo ORDER BY categoria"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
        
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    else:   
        comando_SQL = "SELECT * FROM produtos"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
       

    vendas.tableWidget.setRowCount(len(dados_lidos))
    vendas.tableWidget.setColumnCount(6)    

    linha = vendas.tableWidget.currentRow()
    vendas.tableWidget.removeRow(linha)

    

    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE codigo="+ str(valor_id))

def gerar_pdf():

    cursor = banco.cursor()    

    
    if vendas.rbEstoqueMinimoEstoque.isChecked():
        

        comando_SQL = "SELECT * FROM produtos WHERE quantidade <= estoque_minimo ORDER BY quantidade"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
       
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    elif vendas.rbCategoriaEstoque.isChecked():
     

        comando_SQL = "SELECT * FROM produtos GROUP BY codigo ORDER BY categoria"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
        
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    else:   
        comando_SQL = "SELECT * FROM produtos"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
       
        vendas.tableWidget.setRowCount(len(dados_lidos))
        vendas.tableWidget.setColumnCount(6)    

    
    y = 0
    pdf = canvas.Canvas("Produtos_Cadastrados.pdf")
    pdf.setFont("Times-Bold", 14)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(10,750, "CODIGO")
    pdf.drawString(110,750, "PRODUTO")
    pdf.drawString(210,750, "CATEGORIA")
    pdf.drawString(310,750, "ESTOQUE MINIMO")
    pdf.drawString(410,750, "QUANTIDADE")
    pdf.drawString(510,750, "PREÇO")


    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(510,750 - y, str(dados_lidos[i][5]))


    pdf.save()
    #print("PDF FOI GERADO COM SUCESSO!")
    msgBox = QMessageBox()
    msgBox.setText("PDF FOI GERADO COM SUCESSO!")
    msgBox.open()
    msgBox.exec_()
    
def fechar_app():
    vendas.close()

#===============================botoes ===================================================================

vendas.btBuscarProdutoVenda.clicked.connect(venderProdutos)


vendas.btCadastrarCadastro.clicked.connect(cadastrarProduto)


vendas.btPesquisarEstoque.clicked.connect(consultarEstoque)
vendas.btEditarEstoque.clicked.connect(editar_dados)
vendas.btExcluirEstoque.clicked.connect(excluir_dados)
vendas.btPDF.clicked.connect(gerar_pdf)

tela_editar.btSalvarEditar.clicked.connect(salvar_valor_editado)


vendas.btFechar.clicked.connect(fechar_app)


















#===============================RODAR APLICAÇÃO =============================================

vendas.show()
app.exec()
