# ====== Importação de bibliotecas ====== #
#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash,  session
from models.produto import Produto
from models.sensor import Sensor
from models.usuario import Usuario
from models.lista_compra import Lista_compra
from models.login import Login
from models.fornecedor import Fornecedor
from models.animal import Animal
from models.pedido_entrada import Pedido_entrada
from models.gerenciamento_perfil import GerenciamentoPerfil
from models.informacao_produto import Informacao_Produto
from models.pedido_saida import Pedido_saida
from models.pesquisa import Pesquisa
from datetime import datetime



# definição da variavel app
app = Flask(__name__)

# Chave secreta usada na validação
app.secret_key = "25713|TFZjE1B6p5Q21TSHCOs9Xre7GB9Vwc0P"


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
    

def converter_data(data_str):
    formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']  # aceita vários formatos
    
    for formato in formatos:
        try:
            return datetime.strptime(data_str.strip(), formato).strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return None


# ====== Pegando os dados do Front End ====== #

def get_animal_form():
    return{
        "animal_especie": request.form.get("especie", "").strip(),
        "animal_sexo": request.form.get("sexo", "").strip(),
        "animal_idade": request.form.get("faixa_etaria", "").strip(),  
        "animal_raca": request.form.get("raca", "").strip(),
        "animal_identificacao": request.form.get("identificacao_animal", "").strip(),
    }

# ====== Pegando os dados de produto ====== #
def get_produto_form(): 
    return {
        "produto_nome": request.form.get("nome", "").strip(),
        "produto_descricao": request.form.get("descricao", "").strip(),
        "produto_categoria": request.form.get("categoria", "").strip(),
        "usuario_usuario_id": session["usuario_id"],
    }


# ====== Pegando os dados de pedidos ====== #
def get_pedido_saida_form():
    return {
        "pedido_saida_nome": request.form.get("nome_produto", "").strip(),
        "produto_id": to_int(request.form.get("produto_id")),
        "pedido_saida_data": converter_data(request.form.get("categoria", "").strip()),
        "pedido_saida_status": request.form.get("status", "").strip(),
        "animal_animal_id": to_int(request.form.get("quantidade"))
    }

def get_pedido_entrada_form():
    return {
        "pedido_entrada_nome": request.form.get("nome_produto", "").strip(),
        "pedido_entrada_data":converter_data( request.form.get("data", "").strip()),
        "pedido_entrada_status": request.form.get("status", "").strip(),
        "fornecedor_fornecedor_id": request.form.get('fornecedor_id')
    }

# ====== Pegando os dados do usuario ====== #
def get_usuario_form():
    return{
        "usuario_nome": request.form.get("nome", "").strip(),
        "usuario_email": request.form.get("email", "").strip(),
        "usuario_cpf":request.form.get("cpf", "").strip(),
        "usuario_senha":request.form.get("senha", "").strip(),
        "usuario_cargo": request.form.get("cargo", "").strip(),
        "usuario_confirmar_senha": request.form.get("confirmar_senha", "").strip()
    }

# ====== Pegando os dados para o login ====== #
def get_login_form():
    return{
        "login_email": request.form.get("email", "").strip(),
        "login_senha":request.form.get("senha", "").strip(),
    }

# ====== Pegando os dados para o cadastro de sensores ====== #
def get_sensor_form():
    return{
        "sensor_nome": request.form.get("sensor_nome", "").strip(),
        "sensor_descricao":request.form.get("sensor_descricao", "").strip(),
        "sensor_modelo": request.form.get("sensor_modelo", "").strip(),
        "sensor_voltagem": request.form.get("sensor_voltagem", "").strip(),
        "sensor_n_serie": request.form.get("sensor_n_serie", "").strip(),
        "sensor_tipo_conexao" : (request.form.get("sensor_tipo_conexao", "")),
        "sensor_localizacao": request.form.get("sensor_localizacao", "").strip(),
    }

# ====== Pegando os dados para cadastro de fornecedor ======#

def get_fornecedor_form():
    return {
        "nome": request.form.get("fornecedor_nome", "").strip(),
        "cnpj": (request.form.get("fornecedor_cnpj", "")),
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
    return{
        "usuario_nome": request.form.get("usuario_nome", "").strip(),
        "usuario_email": request.form.get("usuario_email", "").strip(),  
        "usuario_cargo": request.form.get("usuario_cargo", "").strip(),
        "usuario_id": request.form.get("usuario_id", ""),
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
@app.route("/inicial")
def inicial():
    usuario_id = session.get("usuario_id") 
    produtos  = Produto.buscar_todo_produto()
    

    if usuario_id:
        usuario_completo = Usuario.buscar_usuario_por_id(usuario_id) 
        return render_template("tela_inicial.html", usuario=usuario_completo, produtos=produtos)
    

    return redirect('/login')




# ====== Endpoints para o cadastro de produtos ====== #

# ===== Rotas tela de produto ====== #
@app.route("/produtos")
def produtos():

    try:
        produtos = Produto.buscar_todo_produto()

        if not produtos:
            flash("Nenhum produto encontrado", "danger")
            return render_template("produto_cadastrados.html")

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
        produto.gravar_produto()
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
@app.route("/produto/excluir/<int:produto_id>", methods=["DELETE"])
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
        return redirect(url_for("novo_sensor"))
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
@app.route("/sensor/excluir/<int:sensor_id>", methods=["DELETE"])
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
        return redirect(url_for("novo_lista_compra"))
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

# ======= Editar dados lista dr compra ======= #
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


    try:
        pesquisa_item = Pesquisa.buscar_tudo_pesquisa(q)
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
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("novo_login"))




# ======== Endpoint animal ======= #

# ========= Animais cadastrados =====#
@app.route("/animal")
def animal():

    return render_template("cadastro_animais.html")

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
        return redirect(url_for("novo_animal"))
        
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
@app.route("/animal/excluir/<int:animal_id>", methods=["DELETE"])
def excluir_animal(id):
    try:
        Animal.deletar_animal(id)
        flash("Animal excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir Animal: {e}", "danger")
    return redirect(url_for("animal"))




# ======= Endpoints fornecedor ====== #

# ======= Formulário de cadastro de fornecedor ===== #
@app.route("/fornecedor/novo")
def fornecedor_novo():
    return render_template("cadastro_fornecedor.html")

# ======= Salvar dados fornecedor ===== #
@app.route("/fornecedor/salvar", methods=["POST"])
def gravar_fornecedor():
    dados = get_fornecedor_form()
    fornecedor = Fornecedor(**dados)
    erros = fornecedor.validar_fornecedor()

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
    


    
# ========= Endpoint gerenciamento de perfil ======= #

# ===== Formulário atualizar dados do usuario ====== #
@app.route("/gerenciar_perfil/<int:usuario_id>", methods=["GET"])
def gerenciar_perfil_atualizar(usuario_id):

    try:
        dados_usuario = GerenciamentoPerfil.buscar_por_id(usuario_id)

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

    usuario_id  = dados.get("usuario_id")
    dados_usuario = GerenciamentoPerfil.buscar_por_id(usuario_id)

    try:
        if erros:
            flash(erros, "danger")
            return render_template("gerenciamento_perfil.html", login=dados, usuario=dados_usuario) 

        atualizar.atualizar_usuario(usuario_id) 

        flash("Dados atualizados.", "success")
        return redirect(url_for("gerenciar_perfil_atualizar", usuario_id=usuario_id))  

    except Exception as e:
        flash(f"Erro ao atualizar dados: {str(e)}", "danger")  
        return render_template("gerenciamento_perfil.html", login=dados, usuario=dados_usuario)
    
# ====== Excluindo usuario ======#
@app.route("/gerenciar_perfil/excluir/<int:usuario_id>", methods=["POST"])
def excluir_usuario(usuario_id):
    try:
        Usuario.deletar_usuario(usuario_id)
        flash("Usuario excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir Usuario: {e}", "danger")
    return redirect(url_for("novo_login"))


# ======== Endpoint entrada produto ====== #

@app.route("/pedido")
def pedido():
    fornecedor = Fornecedor.buscar_fornecedor()
    return render_template("pedido.html", fornecedor=fornecedor)

# ===== salvar entrada de pedidos ===== #
@app.route("/pedido/salvar", methods=["GET", "POST"])
def pedido_salvar():

    dados_entrado = get_pedido_entrada_form()
    dados_saida = get_pedido_saida_form()
    entrada = Pedido_entrada(**dados_entrado)
    saida = Pedido_saida(**dados_saida)
    erros = entrada.validar_pedido_entrada()

    try:

        if erros:
            flash(erros, "danger")
            return render_template("pedido.html")

        entrada.gravar_pedido_entrada()


        flash("Entrada cadastrada.", "success")
        return redirect(url_for("pedido"))

    except Exception as e:
        flash(f"Erro ao cadastrar entrada", "danger")
        return render_template("pedido.html")
    
# ======= Relatorio ======= #

@app.route("/relatorio")
def relatorio():
    try:
        lista_compra = Lista_compra.buscar_lista_compra()
        return render_template("relatorio.html", lista_compra=lista_compra)
    except ValueError as e :
        flash(e, "danger")
        return render_template("relatorio.html")



# ====== Executar codigo ======#
if __name__ == "__main__":
    app.run(debug=True)