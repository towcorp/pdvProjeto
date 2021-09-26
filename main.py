from re import template
from PyQt5 import  uic,QtWidgets,QtGui
from PyQt5.QtCore import dec
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QMessageBox
from datetime import date

import mysql.connector
from reportlab.pdfgen import canvas

app=QtWidgets.QApplication([])
vendas=uic.loadUi("vendas.ui")
tela_editar=uic.loadUi('menu_editar.ui')
tela_recibo=uic.loadUi('recibo.ui')
vendas.vendas = QTabWidget()

#=========================CONECTAR BANCO DE DADOS============================================
numero_id = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123",
    database="estoque_produtos"
)



#=========================PAGINA VENDAS ======================================================

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

            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('VALOR INVALIDO')
            msgBox.setText("PRODUTO NÃO CADASTRADO!")
            msgBox.open()
            msgBox.exec_()
            vendas.cpPesquisaVenda.setText('')
            
  
  
    else:

        try:
            item = vendas.cpPesquisaVenda.text()

            comando_SQL = "SELECT * FROM produtos WHERE codigo = {}".format(item)
            cursor.execute(comando_SQL)
            dados_lidos = cursor.fetchall()
        
            
            vendas.lbItemVenda.setText(dados_lidos[0][1])


        except:

            # CAIXA DE MENSAGEM E CLEAR CAMPO DE BUSCA
            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('VALOR INVALIDO')
            msgBox.setText("PRODUTO NÃO CADASTRADO!")
            msgBox.open()
            msgBox.exec_()
            vendas.cpPesquisaVenda.setText('')
    
    return dados_lidos
 
def adicionar_item():

    cursor = banco.cursor()
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

        soma = round((float(qtde) * float(linha4)), 2)
        linha5 = round(soma, 2)

        
        
 
    else:
        print('erro')


    comando_SQL = 'SELECT quantidade FROM produtos WHERE codigo="{}"'.format(str(linha1))
    cursor.execute(comando_SQL)
    consultaQtd = cursor.fetchall()

    qtde = vendas.cpQuantidadeVenda.text()
    qtdade = consultaQtd[0][0]

    

    
    if int(qtdade) < int(qtde):
        print('consulte quantidade no estoque')
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setWindowTitle('QUANTIDADE FORA DE ESTOQUE')
        msgBox.setText(f'QUANTIDADE EM ESTOQUE: {str(qtdade)}')
        msgBox.open()
        msgBox.exec_()
        
    else:
        print('OK')

        comando_SQL = "INSERT INTO vendasUnitarias(codigo,item,quantidade,preco_unitario, total) VALUES(%s,%s,%s,%s,%s)" 
        dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5))
        cursor.execute(comando_SQL,dados)
        banco.commit()


        vendas.tableWidget_2.setRowCount(len(lista))
        vendas.tableWidget_2.setColumnCount(6)





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
        
        vendas.lbPrecoTotalVenda.setText(str(resultado[0][0]))

        vendas.lbItemVenda.setText('')
        vendas.cpQuantidadeVenda.setText('')
        vendas.cpPesquisaVenda.setText('')
        atualizar_tela_vendas()




def cancelar_compra():
    cursor = banco.cursor()
    comando_SQL = "TRUNCATE TABLE vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    vendas.tableWidget_2.setRowCount(len(dados_lidos))
    vendas.tableWidget_2.setColumnCount(6)  

    vendas.lbPrecoTotalVenda.setText('0,00')
    



    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setWindowTitle('COMPRA CANCELADA')
    msgBox.setText("SUA COMPRA FOI CANCELADA")
    msgBox.open()
    msgBox.exec_()

def retirar_item():

    linha = vendas.tableWidget_2.currentRow()
    vendas.tableWidget_2.removeRow(linha)

    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
       
    
    
    #vendas.tableWidget_2.setRowCount(len(dados_lidos))
    #vendas.tableWidget_2.setColumnCount(6)    
   

    valor_id = dados_lidos[linha][0]
    
    comando_SQL = 'DELETE FROM vendasUnitarias WHERE id="{}"'.format(str(valor_id))
    cursor.execute(comando_SQL)


    comando_SQL = "SELECT sum(total) FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    resultado = cursor.fetchall()
    

    vendas.lbPrecoTotalVenda.setText(str(resultado[0][0]))

    vendas.lbItemVenda.setText('')
    vendas.cpQuantidadeVenda.setText('')
    vendas.cpPesquisaVenda.text('')
    atualizar_tela_vendas()

def pagamento():

    tela_recibo.show()

    if vendas.cbFormaPagamentoVenda.currentText() == 'CARTAO CREDITO' :

        tela_recibo.lbFormaPagar.setText('CARTAO CREDITO')
        forma_pagamento = 'CARTAO CREDITO'

    elif vendas.cbFormaPagamentoVenda.currentText() == 'CARTAO DEBITO' :
        
        tela_recibo.lbFormaPagar.setText('CARTAO DEBITO')
        forma_pagamento = 'CARTAO DEBITO'

    else:

        tela_recibo.lbFormaPagar.setText('DINHEIRO')
        forma_pagamento = 'DINHEIRO'


    #----------------------------------------------------------------
    cursor = banco.cursor()
    #---------------------------------------------------------------------
    # parte visual da tela
    comando_SQL = "SELECT item,quantidade,total FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    tela_recibo.show()

    tela_recibo.tableWidget_3.setRowCount(len(dados_lidos))
    tela_recibo.tableWidget_3.setColumnCount(3)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
           tela_recibo.tableWidget_3.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 

    
    comando_SQL = "SELECT sum(total) FROM vendasUnitarias"

    cursor.execute(comando_SQL)
    resultado = cursor.fetchall()
    
    tela_recibo.totalRecibo.setText(str(resultado[0][0]))
    #----------------------------------------------------------------------------
    comando_SQL = "SELECT max(fatura_id) FROM Vendas_totais  "
    cursor.execute(comando_SQL)
    ultimo_id = cursor.fetchall()


    try:
        faturaID = str(ultimo_id[0][0]+1)
    except:

        faturaID = 1


    
    dataPagamento = date.today()


    comando_SQL = "INSERT INTO Vendas_totais (fatura_id, data,venda_total,forma_pagamento) VALUES(%s,%s,%s,%s)" 
    dados = (str(faturaID),str(dataPagamento),str(resultado[0][0]),str(forma_pagamento))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    totaisVendidos = cursor.fetchall()




    # salvando dados no banco
    comando_SQL = "SELECT * FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    vendas_lidas = cursor.fetchall()



    for linha in vendas_lidas:

        
        linha1 = faturaID
        linha2 = linha[1]
        linha3 = linha[2]
        linha4 = linha[3]
        linha5 = linha[4]
        linha6 = linha[5]
        linha7 = dataPagamento
        
        
        comando_SQL = "INSERT INTO vendasGerais (id_recibo,cod_produto,produto,quantidade,preco_unitario,preco_total,data_compra) VALUES(%s,%s,%s,%s,%s,%s,%s)" 
        dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5),str(linha6),str(linha7))
        cursor.execute(comando_SQL,dados)
        banco.commit()

    # ATUALIZAR eSTOQUE
        comando_SQL = 'SELECT quantidade FROM produtos WHERE codigo={}'.format(str(linha2))
        cursor.execute(comando_SQL)
        consultaQtd = cursor.fetchall()

        qtde = linha4
        qtdade = consultaQtd[0][0]
  
        qtdeNova = qtdade-qtde
        comando_SQL = 'UPDATE produtos SET quantidade = {} WHERE codigo={}'.format(str(qtdeNova), str(linha2))
        cursor.execute(comando_SQL)
        #atualiza_estoque = cursor.fetchall()

        

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

#---------------------RECIBO ---------------------------------------------------------------
def imprimir_recibo():

    cursor = banco.cursor()

    comando_SQL = "SELECT item,quantidade,total FROM vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
       
    vendas.tableWidget.setRowCount(len(dados_lidos))
    vendas.tableWidget.setColumnCount(3)    

    comando_SQL = "SELECT sum(total) FROM vendasUnitarias"

    cursor.execute(comando_SQL)
    resultado = cursor.fetchall()
    tela_recibo.totalRecibo.setText(str(resultado[0][0]))

    
    y = 0
    pdf = canvas.Canvas("RECIBO.pdf")
    pdf.setFont("Times-Bold", 16)
    pdf.drawString(110,800, "RECIBO:")
    pdf.setFont("Times-Bold", 12)

    pdf.drawString(10,750, "PRODUTO")
    pdf.drawString(110,750, "QUANTIDADE")
    pdf.drawString(210,750, "PREÇO TOTAL")
 
    pdf.setFont("Times-Bold", 10)
    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        
    
    pdf.drawString(10,750 - (y+50), '---------------------')    
    pdf.drawString(110,750 - (y+50), '--------------------') 
    pdf.drawString(210,750 - (y+50), '--------------------') 

    pdf.setFont("Times-Bold", 12)
    pdf.drawString(110,750 - (y+100), 'TOTAL :   ')    
    pdf.drawString(210,750 - (y+100), str(tela_recibo.totalRecibo.text()))

    pdf.save()
    #print("PDF FOI GERADO COM SUCESSO!")
    msgBox = QMessageBox()
    
    msgBox.setIcon(QMessageBox.Information)

    msgBox.setWindowTitle('SUCESSO!')
    msgBox.setText("PDF FOI GERADO COM SUCESSO!")
    msgBox.open()
    msgBox.exec_()
    

def fechar_recibo():

    cursor = banco.cursor()
    comando_SQL = "TRUNCATE TABLE vendasUnitarias"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    vendas.tableWidget_2.setRowCount(len(dados_lidos))
    vendas.tableWidget_2.setColumnCount(6)  

    vendas.lbPrecoTotalVenda.setText('0,00')

    '''
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setWindowTitle('SUCESSO')
    msgBox.setText("OBRIGADO PELA COMPRA")
    msgBox.open()
    msgBox.exec_()
    '''
    tela_recibo.close()





#===========================PAGINA CADASTRO =================================================
def cadastrarProduto():

    try:

        linha1 = vendas.cpCodigoCadastro.text()
        linha2 = vendas.cpProdutoCadastro.text().upper()
        linha3 = vendas.cpCategoriaCadastro.text().upper()
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


        msgBox = QMessageBox()
        msgBox.setWindowTitle('SUCESSO!')
        msgBox.setText("PRODUTO CADASTRADO COM SUCESSO!")
        msgBox.open()
        msgBox.exec_()


    except:

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle('VALOR INVALIDO ')
        msgBox.setText('''      
        - - VERIFIQUE OS CAMPOS - 

    CODIGO - Deve ser numerico e unico para cada produto.
    QUANTIDADE - Deve ser um numero Inteiro.
    ESTOQUE MINIMO - Deve ser um numero Inteiro.
    PRECO - Deve ser numerico, use "." para separar.''')
        msgBox.open()
        msgBox.exec_()

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
    #pdf.drawString(200,800, "Produtos cadastrados:")
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
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setWindowTitle('SUCESSO')
    
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
vendas.btPagarVenda.clicked.connect(pagamento)

#BOTOES CADASTRO
vendas.btCadastrarCadastro.clicked.connect(cadastrarProduto)

#BOTOES ESTOQUE
vendas.btPesquisarEstoque.clicked.connect(consultarEstoque)
vendas.btEditarEstoque.clicked.connect(editar_dados)
vendas.btExcluirEstoque.clicked.connect(excluir_dados)
vendas.btPDF.clicked.connect(gerar_pdf)

#BOTAO TELA EDITAR
tela_editar.btSalvarEditar.clicked.connect(salvar_valor_editado)

#BOTAO RECIBO
tela_recibo.btImprimirRecibo.clicked.connect(imprimir_recibo)
tela_recibo.btFecharRecibo.clicked.connect(fechar_recibo)

#FECHAR APLICACAO
vendas.btFechar.clicked.connect(fechar_app)


















#===============================RODAR APLICAÇÃO =============================================

vendas.show()
app.exec()
