# ====== Importação de bibliotecas ====== #
#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash,  session, jsonify, current_app
from models.produto import Produto
from models.sensor import Sensor
from models.usuario import Usuario
from models.lista_compra import Lista_compra
from models.login import Login
from models.fornecedor import Fornecedor
from models.animal import Animal
from models.pedido_entrada import Pedido_entrada, Item_pedido_entrada
from models.gerenciamento_perfil import GerenciamentoPerfil
from models.informacao_produto import Informacao_Produto
from models.pedido_saida import Item_pedido_saida, Pedido_saida
from models.pesquisa import Pesquisa
from datetime import datetime
from models.relatorio import buscar_estoque_db
import base64
from models.contato import Contato
from models.estoque import Estoque
from models.alertas import Alertas


# definição da variavel app
app = Flask(__name__)

# Chave secreta usada na validação
app.secret_key = "27718|LE7dR7xbHO2ygaaOzq2Hh8W07kOle1Mt"


# ====== converter inteiro ====== #
def to_int(value, default=0): 
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# ====== converter decimal ====== #
def to_float(value, default=0.0): 
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
    

# ====== Pegando os dados do Front End ====== #

def get_animal_form():
    return{
        "animal_especie": request.form.get("especie", "").strip(),
        "animal_sexo": request.form.get("sexo", "").strip(),
        "animal_idade": request.form.get("faixa_etaria", "").strip(),  
        "animal_raca": request.form.get("raca", "").strip(),
        "animal_identificacao": request.form.get("identificacao_animal", "").strip(),
    }



def get_contato_form():
    return{
        "contato_nome": request.form.get("nome", "").strip(),
        "contato_email": request.form.get("email", "").strip(),
        "contato_mensagem": request.form.get("texto", "").strip(), 
    }

# ====== Pegando os dados de produto ====== #
def get_produto_form():
    arquivo = request.files.get("imagem")

    if arquivo and arquivo.filename != '':
        produto_imagem = arquivo.filename  
        imagem_tipo = arquivo.content_type
        imagem_blob = arquivo.read()
    else:
        produto_imagem = None
        imagem_tipo = None
        imagem_blob = None
        
    return {
        "produto_nome": request.form.get("nome", "").strip(),
        "produto_descricao": request.form.get("descricao", "").strip(),
        "produto_categoria": request.form.get("categoria", "").strip(),
        "usuario_usuario_id": session["usuario_id"],
        "produto_imagem": produto_imagem,  
        "imagem_tipo": imagem_tipo,
        "imagem_blob": imagem_blob
    }


# ====== Pegando os dados de pedidos ====== #
def get_pedido_saida_form():
    return {
        "pedido_saida_nome": request.form.get("pedido_saida_nome", "").strip(),
        "pedido_saida_data": request.form.get("pedido_saida_data", ""),
        "pedido_entrada_status": request.form.get("pedido_saida_status", "").strip(),
        "animal_animal_id": to_int(request.form.get("animal_animal_id", ""))
    }

def get_pedido_entrada_form():
    return {
        "pedido_entrada_nome": request.form.get("pedido_entrada_nome", "").strip(),
        "pedido_entrada_data": request.form.get("pedido_entrada_data", ""),
        "pedido_entrada_status": request.form.get("pedido_entrada_status", "").strip(),
        "fornecedor_fornecedor_id": request.form.get('fornecedor_fornecedor_id')
    }

def get_item_entrada_form():
    return {
        "produto_produto_id": request.form.getlist("produto_produto_id"),
        "item_pedido_entrada_lote": request.form.getlist("item_pedido_entrada_lote"),
        "item_pedido_entrada_quantidade": request.form.getlist("item_pedido_entrada_quantidade"),
        "item_pedido_entrada_valor_unitario": request.form.getlist("item_pedido_entrada_valor_unitario"),
        "item_pedido_entrada_validade": request.form.getlist("item_pedido_entrada_validade"),
    }

def get_item_saida_form():
    return {
        "produto_produto_id": request.form.getlist("produto_produto_id"),
        "item_pedido_saida_lote": request.form.getlist("item_pedido_saida_lote"),
        "item_pedido_saida_quantidade": request.form.getlist("item_pedido_saida_quantidade"),
    }

# ====== Pegando os dados do usuario ====== #
def get_usuario_form():
    arquivo = request.files.get("imagem")

    if arquivo and arquivo.filename != '':
        usuario_imagem = arquivo.filename
        imagem_tipo = arquivo.content_type
        imagem_blob = arquivo.read()
    else:
        usuario_imagem = None
        imagem_tipo = None
        imagem_blob = None
    return{
        "usuario_nome": request.form.get("nome", "").strip(),
        "usuario_email": request.form.get("email", "").strip(),
        "usuario_cpf":request.form.get("cpf", "").replace(".","").replace("-","").replace("/","").replace(" ",""),
        "usuario_senha":request.form.get("senha", "").strip(),
        "usuario_cargo": request.form.get("cargo", "").strip(),
        "usuario_confirmar_senha": request.form.get("confirmar_senha", "").strip(),
        "usuario_imagem": usuario_imagem,
        "imagem_tipo": imagem_tipo,
        "imagem_blob": imagem_blob
    }

# ====== Pegando os dados para o login ====== #
def get_login_form():
    return{
        "login_email": request.form.get("email", "").strip(),
        "login_senha":request.form.get("senha", "").strip(),
    }

# ====== Pegando os dados para o cadastro de sensores ====== #
def get_sensor_form():
    arquivo = request.files.get("imagem_sensor")

    if arquivo and arquivo.filename != '':
        sensor_imagem = arquivo.filename
        imagem_tipo = arquivo.content_type
        imagem_blob = arquivo.read()
    else:
        sensor_imagem = None
        imagem_tipo = None
        imagem_blob = None

    return {
        "sensor_nome": request.form.get("sensor_nome", "").strip(),
        "sensor_descricao": request.form.get("sensor_descricao", "").strip(),
        "sensor_modelo": request.form.get("sensor_modelo", "").strip(),
        "sensor_voltagem": request.form.get("sensor_voltagem", "").strip(),
        "sensor_n_serie": request.form.get("sensor_n_serie", "").strip(),
        "sensor_tipo_conexao": request.form.get("sensor_tipo_conexao", ""),
        "sensor_localizacao": request.form.get("sensor_localizacao", "").strip(),
        "sensor_imagem": sensor_imagem,
        "imagem_tipo": imagem_tipo,
        "imagem_blob": imagem_blob
    }

# ====== Pegando os dados para cadastro de fornecedor ======#

def get_fornecedor_form():
    return {
        "nome": request.form.get("fornecedor_nome", "").strip(),
        "cnpj": (request.form.get("fornecedor_cnpj", "")).replace(".","").replace("-","").replace("/","").replace(" ",""),
        "endereço":(request.form.get("fornecedor_endereço")),
        "pedido_minimo": to_float( request.form.get("fornecedor_pedido_minimo")),
        "tipo_produtos": request.form.get("fornecedor_tipo_produtos", "").strip(),
    }


def get_lista_compra_form():
    return {
        "lista_compra_nome": request.form.get("nome_produto", "").strip(),
        "lista_compra_quantidade": to_int(request.form.get("quantidade")),
        "lista_compra_valor": to_float(request.form.get("custo_compra")),
        "lista_compra_status": request.form.get("status", "Pendente").strip(),
 
    }

def get_gerenciar_perfil_form():

    arquivo = request.files.get("imagem_usuario")  

    if arquivo and arquivo.filename != '':
        imagem_blob = arquivo.read()
        imagem_tipo = arquivo.content_type
        usuario_imagem = arquivo.filename
    else:
        imagem_blob = None
        imagem_tipo = None
        usuario_imagem = None

    

    return {
        "usuario_nome": request.form.get("usuario_nome", "").strip(),
        "usuario_email": request.form.get("usuario_email", "").strip(),  
        "usuario_cargo": request.form.get("usuario_cargo", "").strip(),
        "usuario_id": request.form.get("usuario_id", ""),
        "usuario_imagem": usuario_imagem,   
        "imagem_tipo": imagem_tipo,         
        "imagem_blob": imagem_blob,          
    }

# ====== Pegando os dados para a pesquisa ====== #
def get_pesquisa_item_form():
    return request.args.get("pesquisa", "").strip()

# ========= Definição das rotas e dos endpoints ========= #

# ====== Rota inicial====== #
@app.route("/")
def index():
    
    return render_template("landingpage.html")

# ====== Tela inicial ====== #

def get_categoria_form():

    if request.method == "POST":
        return request.form.get("categoria")
    return None

@app.route("/inicial", methods=["GET", "POST"])
def inicial():
    usuario_id = session.get("usuario_id") 

    if request.method == 'POST':
        session['categoria_selecionada'] = request.form.get('categoria')
        return redirect(url_for('inicial'))

    categoria_selecionada = session.get('categoria_selecionada')
    try:
        Alertas.contar_baixo_estoque()
        Alertas.contar_vencidos()
        Alertas.contar_data_relativa()
    except Exception as e:
        print(f"Erro ao verificar notificações: {e}")
    try:
        produtos = Produto.buscar_todo_produto()
        total_estoque = Produto.total_estoque()

        # Soma a quantidade em estoque dos produtos da categoria selecionada
        total_categoria = 0
        if categoria_selecionada and produtos:
            for p in produtos:
                cat = p.get('produto_categoria') if isinstance(p, dict) else getattr(p, 'produto_categoria', None)
                qtd = p.get('estoque_quantidade') if isinstance(p, dict) else getattr(p, 'estoque_quantidade', 0)
                
                if cat == categoria_selecionada:
                    total_categoria += int(qtd or 0)

        if usuario_id:
            usuario_completo = Usuario.buscar_usuario_por_id(usuario_id) 
            return render_template(
                "tela_inicial.html", 
                usuario=usuario_completo, 
                produtos=produtos,
                total_estoque=total_estoque, 
                total_categoria=total_categoria,
                categoria_selecionada=categoria_selecionada
            )
        
        return redirect('/login')

    except ValueError as e:
        flash(e, "danger")
        return render_template("tela_inicial.html")

# ====== Contato ====== #
@app.route("/contato/enviar", methods=["POST"])
def contato_enviar():
    dados = get_contato_form()
    novo_contato = Contato(**dados)

    try:
        novo_contato.enviar_email(dados)
        flash("Mensagem enviada com sucesso", "success")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Erro ao enviar mensagem: {e}", "danger")
        return redirect(url_for('home'))
        
# ====== Endpoints para o cadastro de produtos ====== #

# ===== Rotas tela de produto ====== #
@app.route("/produtos")
def produtos():

    try:
        produtos = Produto.buscar_todo_produto()
        if not produtos:
            flash("Nenhum produto encontrado", "danger")
            return render_template("produtos_cadastrados.html", produtos=[])

        return render_template("produtos_cadastrados.html", produtos=produtos)
    except ValueError as e:
        flash(e, "danger")
        return render_template("produtos_cadastrados.html", produtos=[])



# ======= Formulário cadastro de produtos =======#
@app.route("/produto/novo")
def novo_produto():
    return render_template("cadastro_produto.html", produto=None,)


# ====== Cadastrando novos produtos ====== #
@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar_produto()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        return render_template("cadastro_produto.html", produto=dados)

    try:
        id_produto = produto.gravar_produto()
        observacao = ""
        estoque = Estoque(id_produto, observacao, dados["usuario_usuario_id"])
        criar_estoque = estoque.gravar_estoque()

        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("produtos"))
    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "danger")
        return redirect(url_for('produtos'))
    

# ========= Formulário alterar dados produto ======== #
@app.route("/produto/editar/<int:produto_id>", methods=["GET", "POST"] )
def editar_produto(produto_id):

    try:

        produto = Produto.buscar_produto_id(produto_id)

        if not produto:
            flash("Produto não encontrado",  "danger")
            return redirect(url_for('produtos'))
        
        
        return render_template("editar_produtos.html", produto=produto, produto_id=produto_id)
    except ValueError as e :
        flash(e, "danger")
        return redirect(url_for('produtos'))


# ====== Editando cadastros de produtos ====== #
@app.route("/produto/atualizar/<int:produto_id>", methods=["POST"])
def atualizar_produto(produto_id):
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar_produto()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        produto_dict = Produto.buscar_por_id(produto_id)
        return render_template("editar_produtos.html", produto_id=produto_dict)

    try:
        produto_existente = Produto.buscar_por_id(produto_id)
        
        if not produto_existente:
            flash("Produto não encontrado.", "danger")
            return redirect(url_for('produtos'))

        produto.atualizar_produto(produto_id)
        flash("Produto atualizado com sucesso.", "success")
        
        produto_atualizado = Produto.buscar_por_id(produto_id)
        return render_template("editar_produtos.html", produto=produto_atualizado)
    except Exception as e:
        produto_dict = Produto.buscar_por_id(produto_id)
        flash(f"Erro ao atualizar produto: {e}", "danger")
        return render_template("editar_produtos.html", produto=produto_dict)


# ====== Deletando produtos ====== #
@app.route("/produto/excluir/<int:produto_id>")
def excluir_produto(produto_id):
    try:
        Produto.deletar_produto(produto_id)
        flash("Produto excluído com sucesso.", "success")
        return redirect(url_for("produtos"))
    except ValueError as e:
        flash(str(e), "erro")
        return redirect(url_for("produtos"))
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "danger")
        return redirect(url_for("produtos"))
    

# ====== Endpoint informação produto ======= #

@app.route("/informacao_produto/<int:produto_id>")
def informacao_produto_ver(produto_id):

    try :
        produto = Informacao_Produto.buscar_produto_com_estoque(produto_id)
        if not produto:
            flash("Produto não encontrado", "danger")
            return redirect(url_for("produtos"))
        
        return render_template("informacao_produto.html", produto=produto)
    except ValueError as e:
        flash(e, "danger")
        return  redirect(url_for("produtos"))


# ====== Endpoints de cadstro de novos usuarios ======#
@app.route("/usuario")
def usuario():
    return render_template("cadastro_usuario.html", usuario=None)

@app.route("/usuario/novo", methods=['GET', 'POST'])
def novo_usuario():
    return render_template("cadastro_usuario.html", usuario=None)

# ====== Adicionado novo usuario ====== #
@app.route("/usuario/salvar", methods=["POST"])
def salvar_usuario():
    try:
        dados = get_usuario_form()
        usuario = Usuario(**dados)
        erros = usuario.validar_usuario(app.secret_key)

        email = usuario.buscar_email_existe()

        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("cadastro_usuario.html", usuario=dados)
        elif email:
            flash(email, "danger")
            return render_template("cadastro_usuario.html", usuario=dados)

        usuario.gravar_usuario()
        flash("Usuario cadastrado com sucesso.", "success")
        return redirect(url_for("novo_login"))
        
    except Exception as e:
        flash(f"Erro ao cadastrar usuario {e}", "danger")
        return render_template("cadastro_usuario.html", usuario=dados)



# ====== Buscando usuario ====== #
@app.route("/usuario/buscar/<int:id>", methods=["GET"])
def buscar_usuario(id):

    try:
        usuario = Usuario.buscar_usuario_por_id(id)
        if not usuario:
            flash("Usuario não encontrado.", "erro")
            return redirect(url_for("usuario"))
        return render_template("cadastro_usuario.html", usuario=usuario)
    except ValueError as e:
        flash(e, "danger")
        return render_template("cadastro_usuario.html")

# ====== Atualizando dados de usuario ====== #
@app.route("/usuario/atualizar/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    dados = get_usuario_form()
    usuario = Usuario(**dados)
    erros = usuario.validar()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("formulario_usuario.html", usuario=dados)

    try:
        if not Usuario.buscar_usuario_por_id(id):
            flash("Usuario não encontrado.", "erro")
            return redirect(url_for("novo_usuario"))

        usuario.atualizar_usuario(id)
        flash("Usuario atualizado com sucesso.", "sucesso")
        return redirect(url_for("novo_usuario")), 200
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar usuario: {e}", "erro")
        return render_template("cadastro_usuario.html", usuario=dados)

@app.route("/funcionarios/excluir/<int:usuario_id>", methods=["GET"])
def excluir_usuario_funcionario(usuario_id):
    try:
        Usuario.safe_delete(usuario_id)
        flash("Usuário excluído com sucesso!", "success")
        return redirect(url_for("inicial")) 
            
    except ValueError as e:
        flash(str(e), "danger") 
        return redirect(url_for("funcionarios", usuario_id=usuario_id))
        
    except Exception as e:
        flash(f"Erro ao excluir Usuario: {e}", "danger")
        return redirect(url_for("funcionarios", usuario_id=usuario_id))

#======= Tela de Funcionários ====== #
@app.route("/funcionarios")
def funcionarios():

    try:
        funcionarios = Usuario.buscar_usuario()
        if not funcionarios:
            flash("Nenhum funcionario encontrado", "danger")
            return render_template("funcionarios_cadastrados.html")

        return render_template("funcionarios_cadastrados.html", funcionario=funcionarios)
    except ValueError as e:
        flash(e, "danger")
        return render_template("funcionarios_cadastrados.html", funcionario=[])


# ====== Endpoints de sensor ====== #

# ====== Todos os sensores cadastrados ====== #
@app.route("/sensores")
def sensor():
    try:
        sensores =  Sensor.buscar_sensores()
        
        return render_template("sensores_cadastrados.html", sensores=sensores)
    except ValueError as e:
        flash(e, "danger")
        return render_template("sensores_cadastrados.html")

# ====== Formulário de cadastro de senso ======= #
@app.route("/sensor/novo", methods=['GET', 'POST'])
def novo_sensor():
    return render_template("cadastro_sensor.html", sensor=None)

# ====== Adicionado novos sensores ====== #
@app.route("/sensor/salvar", methods=['POST'])
def salvar_sensor():
    dados = get_sensor_form()
    sensor = Sensor(**dados)
    erros = sensor.validar_sensor()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        dados["id"] = id
        return render_template("cadastro_sensor.html", sensor=dados)
    
    try:
        sensor.gravar_sensor()
        flash("Sensor cadastrado com sucesso.", "success")
        return redirect(url_for("sensor"))
    except ValueError as e:
        flash(f"Erro ao cadastrar sensor: {e}", "danger")
        return render_template("Cadastro_sensor.html", sensor=dados)
    
# ====== Informação de sensor ======= #
@app.route("/sensor/informacao/<int:sensor_id>")
def informacao_sensor(sensor_id):

    try:
        sensor = Sensor.buscar_sensor_id(sensor_id)

        if not sensor:
            flash("Sensor nãao encontrato", "danger")
            return redirect(url_for("sensor"))

        return render_template("informacao_sensor.html", sensor=sensor)
    except ValueError as e :
        flash(e, "danger")
        return render_template("sensores_cadastrados.html")

# ====== Formulário editar dados de sensores ====== #
@app.route("/sensor/editar/<int:sensor_id>" ,methods=["GET", "POST"])
def editar_sensor(sensor_id):

    try:
        sensor = Sensor.buscar_por_id(sensor_id)
        if not sensor:
            flash("Sensor não encontrado.", "danger")
            return redirect(url_for("novo_sensor"))
        if sensor["imagem_blob"]:
            sensor["imagem_base64"] = base64.b64encode(sensor["imagem_blob"]).decode("utf-8")
        else:
            sensor["imagem_base64"] = ""
        return render_template("editar_sensores.html", sensor=sensor)
    except ValueError as e:
        flash(e, "danger")
        return render_template("sensores_cadastrados.html")

# ====== Atualizando dados de sensores ====== #
@app.route("/sensor/atualizar/<int:sensor_id>", methods=["POST"])
def atualizar_sensor(sensor_id):
    dados = get_sensor_form()
    atualizar = Sensor(**dados)
    erros = atualizar.validar_sensor()
    dados_sensor = atualizar.buscar_sensor_id(sensor_id)

    try:
        if erros:
            flash(erros, "danger")
            return render_template("editar_sensores.html", sensor=dados_sensor) 

        atualizar.atualizar_sensor(sensor_id) 

        flash("Dados atualizados.", "success")
        return redirect(url_for("editar_sensor", sensor_id=sensor_id))  

    except Exception as e:
        flash(f"Erro ao atualizar dados: {str(e)}", "danger")  
        return render_template("editar_sensores.html", sensor=dados_sensor)
    
# ====== Excluindo  daodos sensores ====== #
@app.route("/sensor/excluir/<int:sensor_id>")
def excluir_sensor(sensor_id):
    try:
        Sensor.deletar_sensor(sensor_id)
        flash("Sensor excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
        return f"erro: {e}"
    except Exception as e:
        flash(f"Erro ao excluir sensor: {e}", "danger")
        return f"erro: {e}"
    return redirect(url_for("sensor"))




# ====== Endpoints da lista de compra ====== #

# ====== Mostrar itens cadastrados na lista de compra ====== #
@app.route("/lista_compra")
def lista_compra():
    try:
        lista_compra = Lista_compra.buscar_lista_compra()
    except ValueError:
        lista_compra = []

    return render_template("lista_compra.html", lista_compra=lista_compra)


# ======= Formulário add item na lista de compra ====== #
@app.route("/lista_compra/novo", methods=["GET", "POST"])
def novo_lista_compra():
    try:
        produtos = Produto.buscar_todo_produto()
        return render_template("adiciona_itens_lista_compra.html", lista_compra=None, produtos=produtos)
    except ValueError as e:
        flash(e, "danger")
        return render_template("lista_compra.html")

# ====== Adicionado novos itens na lista de compra ====== #
@app.route("/lista_compra/salvar", methods=["POST"])
def salvar_lista_compra():
    dados = get_lista_compra_form()
    lista_compra = Lista_compra(**dados)
    erros = lista_compra.validar_lista_compra()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        return render_template("adiciona_itens_lista_compra.html", lista_compra=dados)
    

    try:
        lista_compra.gravar_lista_compra()
        flash("Lista compra feita com sucesso.", "success")
        return redirect(url_for("lista_compra"))
    except Exception as e:
        flash(f"Erro ao criar lista de compras: {e}", "danger")
        return render_template("adiciona_itens_lista_compra.html", lista_compra=dados)
    

# ====== Excluindo itens da lista de compra ======#
@app.route("/lista_compra/excluir/<int:lista_compra_id>", methods=["GET"])
def excluir_lista_compra(lista_compra_id):
    try:
        lista_compra = Lista_compra()
        lista_compra.deletar_lista_compra(lista_compra_id)
        flash("Lista de compra excluíds com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir lista de compra: {e}", "danger")
    return redirect(url_for("lista_compra"))

# ======= Editar dados lista de compra ======= #
@app.route("/listar_compra/atualizar/<int:lista_compra_id>", methods=["POST"])
def atualizar_lista_compra(id):
    dados = get_lista_compra_form()
    lista_compra = Lista_compra(**dados)
    erros = lista_compra.validar_lista_compra()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        dados["id"] = id
        return render_template("lista_compra.html", lista=dados)

    try:
        if not Sensor.buscar_sensor(id):
            flash("Produto não encontrado.", "danger")
            return redirect(url_for("lista_compra"))

        lista_compra.atualizar_lista_compra(id)
        flash("Produtro atualizado com sucesso.", "success")
        return redirect(url_for("lista_compra")), 200
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar Produto: {e}", "danger")
        return render_template("lista_compra.html", lista=dados)




# ====== Endpoints de pesquisas ====== #

# ====== pesquisa ====== #
@app.route("/pesquisa_item/")
def pesquisa():
    q = get_pesquisa_item_form()
    print("pesquisa da vitoria: ",q)
    try:
        pesquisa_item = Pesquisa.buscar_tudo_pesquisa(q)
        

        if pesquisa_item:
            for produto in pesquisa_item:
                if produto["imagem_blob"]:
                    produto["imagem_base64"] = base64.b64encode(produto["imagem_blob"]).decode("utf-8")
                else:
                    produto["imagem_base64"] = ""


        return render_template("pesquisa.html", pesquisa_item=pesquisa_item, q=q)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("inicial"))




# ====== Endpoints para o login ======#

@app.route("/login/novo", methods=["GET", "POST"])
def novo_login():
    status = request.args.get("status")
    return render_template("login.html", status=status)


# ====== Registrar login ======#
@app.route("/login/salvar", methods=["POST"])
def salvar_login():
    dados = get_login_form()
    login = Login(**dados)
    erros = login.validar_login(app.secret_key)

    if erros:
        for erro in erros:
            flash(erro, "danger")
        return render_template("login.html", login=dados)

    try:
        mensagem, usuario = login.autenticar_login()

        if not usuario:
            flash("Usuário não encontrado", "danger")

        session["usuario_id"] = usuario["usuario_id"]
        session["usuario_nome"] = usuario["usuario_nome"]
        session["usuario_cargo"] = usuario["usuario_cargo"]

        return redirect(url_for("inicial"))

    except Exception as e:
        flash(f"Erro ao fazer login", "danger")
        return render_template("login.html", login=dados)

# ======= Logout ======= #
@app.route("/logout")
def logout():
    session.pop('usuario_cargo', None)
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("novo_login"))



# ======== Endpoint animal ======= #

# ========= Animais cadastrados =====#
@app.route("/animal")
def animal():
    try:
        animais = Animal.contar_animal(order_by="animal_id")
        
        return render_template("animais_cadastrados.html", animais=animais)
    except ValueError as e:
        if "não encontrado" in str(e).lower():
            return render_template("animais_cadastrados.html", animais=[])
        
        flash(str(e), "danger")
        return redirect(url_for("novo_animal"))

    

# ======== Formulário cadastro de animal ======= #
@app.route("/animal/novo", methods=['GET', 'POST'])
def novo_animal():
    return render_template("cadastro_animais.html", usuario=None)

# ======= Salvar dados animal =======#
@app.route("/animal/salvar", methods=["POST"])
def salvar_animal():
    try:
        dados = get_animal_form()
        animal = Animal(**dados)
        erros = animal.validar_animal()

        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("cadastro_animais.html", usuario=dados)

        animal.gravar_animal()
        flash("Animal cadastrado com sucesso.", "success")
        return redirect(url_for("animal"))
        
    except Exception as e:
        flash(f"Erro ao cadastrar animal {e}", "danger")
        return render_template("cadastro_animais.html", usuario=dados)


# ======== Buscando animal ====== #
@app.route("/animal/buscar/<int:animal_id>", methods=["GET"])
def buscar_animal(id):
    animal = Animal.buscar_animal_por_id(id)
    if not animal:
        flash("Animal não encontrado.", "erro")
        return redirect(url_for("animal"))
    return render_template("cadastro_usuario.html", animal=animal)

# ====== Excluindo animal compra ======#
@app.route("/animal/excluir/<int:animal_id>", methods=["GET", "POST"])
def excluir_animal(animal_id):
    try:
        Animal.deletar_animal(animal_id)
        flash("Animal excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir Animal: {e}", "danger")
    return redirect(url_for("animal"))




# ======= Endpoints fornecedor ====== #

# ======= Formulário de cadastro de fornecedor ===== #
@app.route("/fornecedor")
def fornecedor_novo():
    try:
        fornecedores = Fornecedor.buscar_fornecedor()
        for i in fornecedores:
            print(i)
        return render_template("fornecedor_cadastrado.html", fornecedores=fornecedores)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("fornecedor_criar"))

@app.route("/fornecedor/novo")
def fornecedor_criar():
    try:
        return render_template("cadastro_fornecedor.html")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("gravar_fornecedor"))

# ======= Salvar dados fornecedor ===== #
@app.route("/fornecedor/salvar", methods=["POST"])
def gravar_fornecedor():
    dados = get_fornecedor_form()
    fornecedor = Fornecedor(**dados)
    erros = fornecedor.validar_fornecedor(app.secret_key)

    try:

        if erros:
            flash(erros, "danger")
            return render_template("cadastro_fornecedor.html")

        fornecedor.gravar_fornecedor()

        flash("Fornecedor cadastrado.", "success")
        return redirect(url_for("fornecedor_novo"))

    except Exception as e:
        flash(f"Erro ao cadastrar fornecedor", "danger")
        return render_template("cadastro_fornecedor.html", login=dados)

@app.route("/fornecedor/excluir/<int:fornecedor_id>", methods=["GET", "POST"])
def excluir_fornecedor(fornecedor_id):
    try:
        f = Fornecedor(None, None, None, None, None)
        f.deletar_fornecedor(fornecedor_id)
        flash("Fornecedor excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir fornecedor: {e}", "danger")
    return redirect(url_for("fornecedor_novo"))

@app.route("/fornecedor/editar/<int:fornecedor_id>" ,methods=["GET", "POST"])
def editar_fornecedor(fornecedor_id):

    try:
        fornecedor = Fornecedor.buscar_por_id(fornecedor_id)
        if not fornecedor:
            flash("Fornecedor não encontrado.", "danger")
            return redirect(url_for("novo_fornecedor"))
        return render_template("editar_fornecedor.html", fornecedor=fornecedor)
    except ValueError as e:
        flash(e, "danger")
        return render_template("fornecedor_cadastrado.html")  


@app.route("/pedido/editar/<int:pedido_id>" ,methods=["GET", "POST"])
def editar_pedido(pedido_id):
    print(pedido_id)
    try:
        pedido = Pedido_entrada.buscar_por_id(pedido_id)
        print(pedido)
        if not pedido:
            flash("Pedido não encontrado.", "danger")
            return redirect(url_for("pedido"))
        return render_template("editar_pedido.html", pedido=pedido)
    except ValueError as e:
        flash(e, "danger")
        return render_template("pedidos_cadastrado.html")



@app.route("/pedido/atualizar/<int:pedido_id>", methods=["GET", "POST"])
def atualizar_pedido(pedido_id):
    try:
        dados_pedido = Fornecedor.buscar_por_id(fornecedor_id)
        if not dados_pedido:
            flash("Pedido não encontrado.", "danger")
            return redirect(url_for("pedido"))
    except Exception as e:
        flash(f"Erro ao buscar pedido: {str(e)}", "danger")
        return redirect(url_for("pedido"))
    if request.method == "POST":
        dados = get_pedido_form()
        atualizar = Pedido(**dados)
        erros = atualizar.validar_fornecedor(current_app.config['SECRET_KEY'])

        try:
            if erros:
                for erro in erros:
                    flash(erro, "danger")
                # Retorna os dados digitados na tentativa para não apagar o formulário
                return render_template("editar_pedido.html", pedido=dados) 

            # Executa a atualização no banco de dados
            atualizar.atualizar_fornecedor(fornecedor_id) 

            flash("Dados atualizados com sucesso.", "success")
            # Correção 4: Redireciona de volta para a rota correta passando o ID certo
            return redirect(url_for("editar_pedido", pedido_id=pedido_id))  

        except Exception as e:
            flash(f"Erro ao atualizar dados: {str(e)}", "danger")  
            # Adicionado fornecedor_id=fornecedor_id no render_template abaixo
            return render_template("editar_pedido.html", pedido=dados, pedido_id=pedido_id)

    # 3. Se for GET, apenas exibe a página com os dados salvos no banco
    return render_template("editar_pedido.html", pedido=dados_pedido)


@app.route("/fornecedor/atualizar/<int:fornecedor_id>", methods=["GET", "POST"])
def atualizar_fornecedor(fornecedor_id):
    try:
        dados_fornecedor = Fornecedor.buscar_por_id(fornecedor_id)
        if not dados_fornecedor:
            flash("Fornecedor não encontrado.", "danger")
            return redirect(url_for("fornecedor_novo"))
    except Exception as e:
        flash(f"Erro ao buscar fornecedor: {str(e)}", "danger")
        return redirect(url_for("fornecedor_novo"))
    if request.method == "POST":
        dados = get_fornecedor_form()
        atualizar = Fornecedor(**dados)
        erros = atualizar.validar_fornecedor(current_app.config['SECRET_KEY'])

        try:
            if erros:
                for erro in erros:
                    flash(erro, "danger")
                # Retorna os dados digitados na tentativa para não apagar o formulário
                return render_template("editar_fornecedor.html", fornecedor=dados) 

            # Executa a atualização no banco de dados
            atualizar.atualizar_fornecedor(fornecedor_id) 

            flash("Dados atualizados com sucesso.", "success")
            # Correção 4: Redireciona de volta para a rota correta passando o ID certo
            return redirect(url_for("editar_fornecedor", fornecedor_id=fornecedor_id))  

        except Exception as e:
            flash(f"Erro ao atualizar dados: {str(e)}", "danger")  
            # Adicionado fornecedor_id=fornecedor_id no render_template abaixo
            return render_template("editar_fornecedor.html", fornecedor=dados, fornecedor_id=fornecedor_id)

    # 3. Se for GET, apenas exibe a página com os dados salvos no banco
    return render_template("editar_fornecedor.html", fornecedor=dados_fornecedor)


#========== Endpoint de erro ======== #
@app.errorhandler(404)
def pagina_nao_encontrado(error):
    return render_template("404.html"), 404

    
# ========= Endpoint gerenciamento de perfil ======= #

# ===== Formulário atualizar dados do usuario ====== #
@app.route("/gerenciar_perfil/<int:usuario_id>", methods=["GET"])
def gerenciar_perfil_atualizar(usuario_id):

    try:
        dados_usuario = GerenciamentoPerfil.buscar_usuario_por_id(usuario_id)

        if dados_usuario.get("imagem_blob"):
            dados_usuario["imagem_base64"] = base64.b64encode(
                dados_usuario["imagem_blob"]
            ).decode("utf-8")

        if not dados_usuario:
            flash("Usuario não encontrdo", "danger")
            return redirect(url_for("novo_usuario"))
        

        return render_template("gerenciamento_perfil.html", usuario=dados_usuario)
    except ValueError as e:
        flash(e, "danger")
        return render_template("tela_inicial.html")

# ======= Salva a atualização ====== #
@app.route("/gerenciar_perfil/salvar", methods=["GET", "POST"])
def gerenciar_perfil_salvar():
    dados = get_gerenciar_perfil_form()
    atualizar = GerenciamentoPerfil(**dados)
    erros = atualizar.validar_perfil(app.secret_key)

    usuario_id = dados.get("usuario_id") or session.get("usuario_id")
    dados_usuario = GerenciamentoPerfil.buscar_por_id(usuario_id) if usuario_id else None

    if not dados_usuario:
        session.clear()
        flash("Usuário não encontrado. Faça login novamente.", "warning")
        return redirect(url_for("novo_login"))  

    try:
        if erros:
            flash(erros, "danger")
            return render_template("gerenciamento_perfil.html", login=dados, usuario=dados_usuario)

        atualizar.atualizar_usuario(usuario_id)
        flash("Dados atualizados.", "success")

        dados_usuario["imagem_base64"] = (
            base64.b64encode(dados_usuario["imagem_blob"]).decode("utf-8")
            if dados_usuario.get("imagem_blob") else None
        )
        return render_template("gerenciamento_perfil.html", login=dados, usuario=dados_usuario)

    except Exception as e:
        flash(f"Erro ao atualizar dados: {str(e)}", "danger")
        return render_template("gerenciamento_perfil.html", login=dados, usuario=dados_usuario)
    
# ====== Excluindo usuario ======#
@app.route("/gerenciar_perfil/excluir/<int:usuario_id>", methods=["POST"])
def excluir_usuario(usuario_id):
    try:
        Usuario.safe_delete(usuario_id)
        session.clear()  
        flash("Usuário excluído com sucesso!", "success")
        return redirect(url_for("novo_login"))  
            
    except ValueError as e:
        flash(str(e), "danger") 
        return redirect(url_for("gerenciar_perfil_atualizar", usuario_id=usuario_id))
        
    except Exception as e:
        flash(f"Erro ao excluir Usuario: {e}", "danger")
        return redirect(url_for("gerenciar_perfil_atualizar", usuario_id=usuario_id))


# ======== Endpoint entrada produto ====== #
@app.route("/pedidos_cadastrados")
def pedidos_cadastrados():
    pedido_entrada = []
    pedido_saida = []
    
    # 1. Tenta buscar pedidos de entrada
    try:
        pedido_entrada = Pedido_entrada.buscar_todo_pedido_entrada(order_by="pedido_entrada_nome") or []
    except ValueError as e:
        if "não encontrado" in str(e).lower():
            pedido_entrada = [] # Banco vazio para entradas
        else:
            flash(f"Erro nas entradas: {str(e)}", "danger")

    # 2. Tenta buscar pedidos de saída
    try:
        pedido_saida = Pedido_saida.buscar_todos_pedidos_saida(order_by="pedido_saida_nome") or []
    except ValueError as e:
        if "não encontrado" in str(e).lower():
            pedido_saida = [] # Banco vazio para saídas
        else:
            flash(f"Erro nas saídas: {str(e)}", "danger")

    # 3. Notifica se ambos estiverem zerados de forma amigável (sem quebrar a tela)
    if not pedido_entrada and not pedido_saida:
        flash("Nenhum pedido de entrada ou saída localizado.", "warning")

    return render_template(
        "pedidos_cadastrados.html", 
        Pedidos_ent=pedido_entrada, 
        Pedidos_saida=pedido_saida
    )



@app.route("/pedido")
def pedido():
    try:
        fornecedor = Fornecedor.buscar_fornecedor()
    except ValueError:
        fornecedor = []

    try:
        produtos = Produto.buscar_todo_produto()
    except ValueError:
        produtos = []

    try:
        animal = Animal.contar_animal()
    except ValueError:
        animal = []

    try:
        lote = Item_pedido_entrada.buscar_item_pedido_entrada()
    except ValueError:
        lote = []

    return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal, lote=lote)


# ===== salvar entrada de pedidos ===== #
@app.route("/pedido/salvar", methods=["GET", "POST"])
def pedido_salvar():
    fornecedor = Fornecedor.buscar_fornecedor()
    produtos = Produto.buscar_todo_produto()

    dados_entrada = get_pedido_entrada_form()
    dados_saida = get_pedido_saida_form()
    item_dados = get_item_entrada_form()
    item_dados_saida = get_item_saida_form()

    if "pedido_entrada_nome" in request.form:
        entrada = Pedido_entrada(**dados_entrada)
        erros_entrada = entrada.validar_pedido_entrada()
        animal = Animal.buscar_animal()

        data_convertida = entrada.converter_data(entrada.pedido_entrada_data)
        if data_convertida:
            entrada.pedido_entrada_data = data_convertida

        if erros_entrada:
            for erro in erros_entrada:
                flash(erro, "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

        # Valida pelo ID retornado do formulário
        produtos_entrada = [p for p in item_dados.get("produto_produto_id", []) if p.strip()]
        if not produtos_entrada:
            flash("Adicione pelo menos um item válido ao pedido.", "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

        tamanhos = [len(v) for v in item_dados.values() if isinstance(v, list)]
        if len(set(tamanhos)) > 1:
            flash("Erro nos dados dos itens — tente adicionar novamente.", "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

        try:
            numero = entrada.gravar_pedido_entrada()

            if not numero:
                flash("Erro ao cadastrar entrada", "danger")
                return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

            itens_validados = []
            erros_itens = []

            for i in range(len(item_dados["produto_produto_id"])):
                prod_id_raw = item_dados["produto_produto_id"][i]
                qtd_raw = item_dados["item_pedido_entrada_quantidade"][i]
                valor_raw = item_dados["item_pedido_entrada_valor_unitario"][i]

                if not prod_id_raw or not qtd_raw or not valor_raw:
                    erros_itens.append(f"Item {i+1}: produto, quantidade e valor unitário são obrigatórios.")
                    continue

                try:
                    produto_id_convertido = int(prod_id_raw)
                    quantidade_convertida = int(qtd_raw)
                    valor_convertido = float(valor_raw)
                except ValueError:
                    erros_itens.append(f"Item {i+1}: ID do produto, quantidade ou valor inválido.")
                    continue

                nome_produto = Produto.buscar_nome_produto(produto_id_convertido)

                dados_do_item = {
                    "produto_produto_id": produto_id_convertido,
                    "item_pedido_entrada_nome": nome_produto,
                    "item_pedido_entrada_lote": item_dados["item_pedido_entrada_lote"][i],
                    "item_pedido_entrada_quantidade": quantidade_convertida,
                    "item_pedido_entrada_validade": item_dados["item_pedido_entrada_validade"][i],
                    "item_pedido_entrada_valor_unitario": valor_convertido,
                    "pedido_entrada_pedido_entrada_id": numero
                }

                item_instanciado = Item_pedido_entrada(**dados_do_item)
                erros_do_item = item_instanciado.validar_item_pedido_entrada()

                if erros_do_item:
                    erros_itens.extend(erros_do_item)
                    continue

                itens_validados.append(item_instanciado)
                item_instanciado.gravar_item_pedido_entrada(numero)

            if erros_itens:
                for erro in erros_itens:
                    flash(erro, "danger")
                return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

            flash("Entrada cadastrada.", "success")
            return redirect(url_for("pedido"))

        except Exception as e:
            flash(f"Erro ao cadastrar entrada: {e}", "danger")
            print(e)
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

    else:
        animal = Animal.contar_animal()
        saida = Pedido_saida(**dados_saida)
        erros_saida = saida.validar_pedido_saida()

        if erros_saida:
            for erro in erros_saida:
                flash(erro, "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

        # Valida pelos IDs de produtos da saída
        produtos_saida = [p for p in item_dados_saida.get("produto_produto_id", []) if p.strip()]
        if not produtos_saida:
            flash("Adicione pelo menos um item válido ao pedido.", "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

        tamanhos = [len(v) for v in item_dados_saida.values() if isinstance(v, list)]
        if len(set(tamanhos)) > 1:
            flash("Erro nos dados dos itens — tente adicionar novamente.", "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

        try:
            numero_saida = saida.gravar_pedido_saida()

            if not numero_saida:
                flash("Erro ao cadastrar saída", "danger")
                return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

            itens_validados_saida = []
            erros_itens_saida = []

            for i in range(len(item_dados_saida["produto_produto_id"])):
                qtd_raw = item_dados_saida["item_pedido_saida_quantidade"][i]
                prod_id_raw = item_dados_saida["produto_produto_id"][i]

                if not prod_id_raw or not qtd_raw:
                    erros_itens_saida.append(f"Item {i+1}: produto e quantidade são obrigatórios.")
                    continue

                try:
                    quantidade_convertida = int(qtd_raw)
                    produto_id_convertido = int(prod_id_raw)
                except ValueError:
                    erros_itens_saida.append(f"Item {i+1}: quantidade ou ID do produto inválido.")
                    continue

                nome_produto = Produto.buscar_nome_produto(produto_id_convertido)

                dados_do_item_saida = {
                    "item_pedido_saida_nome": nome_produto,
                    "item_pedido_saida_lote": item_dados_saida["item_pedido_saida_lote"][i],
                    "item_pedido_saida_quantidade": quantidade_convertida,
                    "pedido_saida_pedido_saida_id": numero_saida,
                    "produto_produto_id": produto_id_convertido
                    
                }

                item_instanciado_saida = Item_pedido_saida(**dados_do_item_saida)
                erros_do_item = item_instanciado_saida.validar_item_pedido_saida()

                if erros_do_item:
                    erros_itens_saida.extend(erros_do_item)
                    continue

                itens_validados_saida.append(item_instanciado_saida)
                item_instanciado_saida.gravar_item_pedido_saida(numero_saida)

            if erros_itens_saida:
                for erro in erros_itens_saida:
                    flash(erro, "danger")
                return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

            flash("Saída cadastrada.", "success")
            return redirect(url_for("pedido"))

        except Exception as e:
            flash(f"Erro ao cadastrar saída: {e}", "danger")
            return render_template("pedido.html", fornecedor=fornecedor, produtos=produtos, animal=animal)

# ======= Relatorio ======= #  
@app.route("/api/relatorio", methods=["GET"])
def api_relatorio():

    try:

        nome = request.args.get("nome", "").strip()
        categoria = request.args.get("categoria", "").strip()
        quantidade = request.args.get("quantidade", "").strip()

        if quantidade:
            try:
                quantidade = int(quantidade)
            except ValueError:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Quantidade inválida."
                }), 400
        else:
            quantidade = None

        if categoria == "vencidos":
            produtos = Produto.buscar_vencidos_db(
                nome=nome,
                quantidade=quantidade
            )
        else:
            produtos = buscar_estoque_db(
                nome=nome,
                categoria=categoria,
                quantidade=quantidade
            )

        return jsonify({
            "sucesso": True,
            "total": len(produtos),
            "produtos": produtos
        })

    except Exception as erro:
        return jsonify({
            "sucesso": False,
            "mensagem": str(erro)
        }), 500


@app.route("/relatorio", methods=["GET"])
def relatorio():

    try:
        sensores = Sensor.contar_sensores()
    except ValueError:
        sensores = 0

    try:
        animais = Animal.contar_animais()
    except ValueError:
        animais = 0

    try:
        produtos = Produto.contar_produtos()
    except ValueError:
        produtos = 0

    try:
        vencidos = len(Produto.buscar_vencidos_db())
    except Exception:
        vencidos = 0

    return render_template(
        "relatorio.html",
        animal=animais,
        sensor=sensores,
        produto=produtos,
        vencido=vencidos
    )
    
@app.route("/relatorio/lista_compra/excluir/<int:lista_compra_id>", methods=["GET"])
def excluir_lista_compra_relatorio(lista_compra_id):
    try:
        lista_compra = Lista_compra()
        lista_compra.deletar_lista_compra(lista_compra_id)
        flash("Item excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir lista de compra: {e}", "danger")
    return redirect(url_for("relatorio"))

#====== Rotas Noficicacoes ========#
@app.route("/api/notificacoes")
def api_notificacoes():
    try:
        notificacoes = Alertas.buscar_pendentes()
        return jsonify({
            "sucesso": True,
            "total": len(notificacoes),
            "notificacoes": notificacoes
        })
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 500

@app.route("/api/notificacoes/verificar", methods=["POST"])
def verificar_notificacoes():
    try:
        Alertas.contar_baixo_estoque()
        Alertas.contar_vencidos()
        Alertas.contar_data_relativa()
        return jsonify({"sucesso": True})
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 500


# ====== Executar codigo ======#
if __name__ == "__main__":
    app.run(debug=True)