from PyQt5 import  uic,QtWidgets,QtGui
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

def pesquisar_produto():
    
    cursor = banco.cursor() 
 
    if vendas.rbProdutoVenda.isChecked():
        
        try:
        
            item = vendas.cpPesquisaVenda.text()
            
            comando_SQL = "SELECT * FROM produtos WHERE produto LIKE '{}'".format(item)
            
            cursor.execute(comando_SQL)
            
            dados_lidos = cursor.fetchall()

            

            vendas.lbItemVenda.setText(dados_lidos[0][1])

        except IndexError:

            
            vendas.lbItemVenda.setText('NÃO ENCONTADO')
            
  
  
    else:

        try:
            item = vendas.cpPesquisaVenda.text()

            comando_SQL = "SELECT * FROM produtos WHERE codigo = {}".format(item)
            cursor.execute(comando_SQL)
            dados_lidos = cursor.fetchall()
        
            
            vendas.lbItemVenda.setText(dados_lidos[0][1])


        except IndexError:

            
            vendas.lbItemVenda.setText('NÃO ENCONTADO')
    

    return dados_lidos
 
def adicionar_item():

    lista = pesquisar_produto()

    

    if lista:
        linha1 = lista[0][0]
        linha2 = lista[0][1]
        
        qtde = vendas.cpQuantidadeVenda.text()
        if vendas.cpQuantidadeVenda.text() == '':
            qtde = 1
            linha3 = qtde
            
        
        else:
        
            
            linha3 = qtde


        linha4 = lista[0][5]

        soma = round((float(qtde) * linha4),2)
        linha5 = soma

        
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO vendasUnitarias(codigo,item,quantidade,preco_unitario, total) VALUES(%s,%s,%s,%s,%s)" 
        dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5))
        cursor.execute(comando_SQL,dados)
        banco.commit()


        vendas.tableWidget_2.setRowCount(len(lista))
        vendas.tableWidget_2.setColumnCount(6)
        

        
                
    else:
        print('erro')


    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    vendas.tableWidget_2.setRowCount(len(dados_lidos))
    vendas.tableWidget_2.setColumnCount(6)  

    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            vendas.tableWidget_2.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    
    comando_SQL = "SELECT sum(total) FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    resultado = cursor.fetchall()
    print(resultado)

    vendas.lbPrecoTotalVenda.setText(str(resultado[0][0]))

    vendas.lbItemVenda.setText('')
    vendas.cpQuantidadeVenda.setText('')
    vendas.cpPesquisaVenda.text('')
    atualizar_tela_vendas()

def cancelar_compra():
    cursor = banco.cursor()
    comando_SQL = "TRUNCATE TABLE vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    vendas.tableWidget_2.setRowCount(len(dados_lidos))
    vendas.tableWidget_2.setColumnCount(6)  

    vendas.lbPrecoTotalVenda.setText('0,00')
    

def retirar_item():

    linha = vendas.tableWidget_2.currentRow()
    vendas.tableWidget_2.removeRow(linha)

    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
       
    print(linha)
    print(dados_lidos)
    #vendas.tableWidget_2.setRowCount(len(dados_lidos))
    #vendas.tableWidget_2.setColumnCount(6)    
   

    valor_id = dados_lidos[linha][0]
    print(valor_id)
    comando_SQL = 'DELETE FROM vendasUnitarias WHERE id="{}"'.format(str(valor_id))
    cursor.execute(comando_SQL)


    comando_SQL = "SELECT sum(total) FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    resultado = cursor.fetchall()
    print(resultado)

    vendas.lbPrecoTotalVenda.setText(str(resultado[0][0]))

    vendas.lbItemVenda.setText('')
    vendas.cpQuantidadeVenda.setText('')
    vendas.cpPesquisaVenda.text('')
    atualizar_tela_vendas()

def pagamento():
    pass


def atualizar_tela_vendas():
    vendas.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    vendas.tableWidget_2.setRowCount(len(dados_lidos))
    vendas.tableWidget_2.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
           vendas.tableWidget_2.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 


#===========================PAGINA CADASTRO =================================================
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






#===========================PAGINA ESTOQUE ====================================================
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

    linha = vendas.tableWidget.currentRow()
    vendas.tableWidget.removeRow(linha)

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

#BOTOES VENDAS
vendas.btBuscarProdutoVenda.clicked.connect(pesquisar_produto)
vendas.btAdicionarVenda.clicked.connect(adicionar_item)
vendas.btCancelarCompraVenda.clicked.connect(cancelar_compra)
vendas.btRetirarItemVenda.clicked.connect(retirar_item)
#vendas.btPagarVenda.clicked.connect(venderProdutos)

#BOTOES CADASTRO
vendas.btCadastrarCadastro.clicked.connect(cadastrarProduto)

#BOTOES ESTOQUE
vendas.btPesquisarEstoque.clicked.connect(consultarEstoque)
vendas.btEditarEstoque.clicked.connect(editar_dados)
vendas.btExcluirEstoque.clicked.connect(excluir_dados)
vendas.btPDF.clicked.connect(gerar_pdf)

#BOTAO TELA EDITAR
tela_editar.btSalvarEditar.clicked.connect(salvar_valor_editado)


#FECHAR APLICACAO
vendas.btFechar.clicked.connect(fechar_app)


















#===============================RODAR APLICAÇÃO =============================================

vendas.show()
app.exec()
