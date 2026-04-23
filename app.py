# ====== Importação de bibliotecas ====== #
#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash
from models.produto import Produto
from models.movimentacao import Movimentacao
from models.sensor import Sensor
from models.usuario import Usuario
from models.lista_compra import Lista_compra
from models.login import Login

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


# ====== Pegando os dados do Front End ====== #

# ====== Pegando os dados de produto ====== #
def get_produto_form(): 
    return {
        "produto_nome": request.form.get("nome", "").strip(),
        "produto_descricao": request.form.get("descricao", "").strip(),
        "produto_categoria": request.form.get("categoria", "").strip(),
        "usuario_usuario_id": request.form.get("usuario_usuario_id", "").strip()
    }


# ====== Pegando os dados de pedidos ====== #
def get_pedido_form():
    return {
        "nome_produto": request.form.get("nome_produto", "").strip(),
        "produto_id": to_int(request.form.get("produto_id")),
        "categoria": request.form.get("categoria", "").strip(),
        "quantidade": to_int(request.form.get("quantidade")),
        "observacao": request.form.get("observacao", "").strip(),
        "tipo_movimentacao": request.form.get("tipo_movimentacao", "").strip(),
        "data_movimentacao":  request.form.get("data_movimentacao", "").strip()
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
        "sensor_nome": request.form.get("nome", "").strip(),
        "sensor_descricao":request.form.get("descricao", "").strip(),
        "sensor_modelo": request.form.get("modelo", "").strip(),
        "sensor_voltagem": request.form.get("voltagem", "").strip(),
        "sensor_n_serie": request.form.get("numero_serie", "").strip(),
        "sensor_tipo_conexao" : to_int(request.form.get("conexao")),
        "sensor_localizacao": request.form.get("localizacao", "").strip(),
    }

# ====== Pegando os dados para a lista de compra ======#
def get_lista_compra_form():
        return{
        "nome_produto": request.form.get("nome_produto", "").strip(),
        "produto_id": to_int(request.form.get("produto_id")),
        "quantidade": to_int(request.form.get("quantidade")),
        "custo_compra": to_float(request.form.get("custo_compra")),
    }

# ====== Pegando os dados para a pesquisa ====== #
def get_pesquisa_item_form():
        return{
        "nome_produto": request.form.get("nome_produto", "").strip(),
    }

# ========= Definição das rotas e dos endpoints ========= #

# ====== Rota de teste ====== #
@app.route("/")
def index():
    #produtos_baixo = Produto.low_stock()
    return render_template("landingpage.html")


# ====== Endpoints para o cadastro de produtos ====== #

# ===== Buscando produtos ====== #
@app.route("/produtos", methods=["GET"])
def produtos():
    return render_template("produtos.html", produtos=Produto.buscar_todo_produto(order_by="produto_nome"))


@app.route("/produto/novo")
def novo_produto():
    return render_template("formulario_produto.html", produto=None)

# ====== Cadaastrando novos produtos ====== #
@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        #return render_template("formulario_produto.html", produto=dados)
            return f"Erro: {erro}"

    try:
        produto.gravar_produto()
        flash("Produto cadastrado com sucesso.", "sucesso")
        return redirect(url_for("produtos")), 200
    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "erro")
        #return render_template("formulario_produto.html", produto=dados)
        return f"Erro: {e}"

'''
@app.route("/produto/editar/<int:id>")
def editar_produto(id):
    produto = Produto.find_by_id(id)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("produtos"))
    return render_template("formulario_produto.html", produto=produto)'''

# ====== Editando cadastros de produtos ======#
@app.route("/produto/atualizar/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        #return render_template("formulario_produto.html", produto=dados)
        return f"Erro: {erro}"

    try:
        if not Produto.buscar_por_id(id):
            flash("Produto não encontrado.", "erro")
            return redirect(url_for("produtos"))

        produto.atualizar_produto(id)
        flash("Produto atualizado com sucesso.", "sucesso")
        return redirect(url_for("produtos")), 200
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar produto: {e}", "erro")
        #return render_template("formulario_produto.html", produto=dados)
        return f"Erro: {e}"

# ====== Deletando produtos ====== #
@app.route("/produto/excluir/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    try:
        Produto.deletar_produto(id)
        flash("Produto excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
        return f"erro: {e}"
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "erro")
        return f"erro: {e}"
    return redirect(url_for("produtos")), 200

# ====== Endpoints de pedido ====== #

'''
@app.route("/pedidos")
def pedidos():
    return render_template("pedidos.html", pedidos=PedidoMovimentacao.find_all_with_product())


@app.route("/pedido/novo/<tipo>/<int:produto_id>")
def novo_pedido(tipo, produto_id):
    produto = Produto.find_by_id(produto_id)
    tipo = tipo.upper()

    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("produtos"))

    if tipo not in ["ENTRADA", "SAIDA"]:
        flash("Tipo de pedido inválido.", "erro")
        return redirect(url_for("produtos"))

    return render_template("formulario_pedido.html", produto=produto, tipo=tipo, pedido=None)


@app.route("/pedido/salvar", methods=["POST"])
def salvar_pedido():
    dados = get_pedido_form()
    produto = Produto.find_by_id(dados["produto_id"])
    pedido = PedidoMovimentacao(**dados)
    erros = pedido.validate()

    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("produtos"))

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("formulario_pedido.html", produto=produto, tipo=dados["tipo"], pedido=dados)

    try:
        pedido.insert()
        flash("Pedido criado com sucesso.", "sucesso")
        return redirect(url_for("pedidos"))
    except Exception as e:
        flash(f"Erro ao criar pedido: {e}", "erro")
        return render_template("formulario_pedido.html", produto=produto, tipo=dados["tipo"], pedido=dados)


@app.route("/pedido/processar/<int:id>")
def processar_pedido(id):
    try:
        mensagem = PedidoMovimentacao.processar(id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao processar pedido: {e}", "erro")
    return redirect(url_for("pedidos"))


@app.route("/pedido/cancelar/<int:id>")
def cancelar_pedido(id):
    try:
        mensagem = PedidoMovimentacao.cancelar(id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao cancelar pedido: {e}", "erro")
    return redirect(url_for("pedidos"))
'''


# ====== Endpoint de movimentação de produtos ======#

@app.route("/movimentacoes")
def movimentacoes():
    return render_template("movimentacoes.html", movimentacoes=Movimentacao.find_all_with_product())


# ====== Endpoints de cadstro de novos usuarios ======#


@app.route("/usuario/novo", methods=['GET', 'POST'])
def novo_usuario():
    return render_template("cadastro_usuario.html", usuario=None)

# ====== Adicionado novo usuario ====== #
@app.route("/usuario/salvar", methods=["POST"])
def salvar_usuario():
    try:
        dados = get_usuario_form()
        usuario = Usuario(**dados)
        erros = usuario.validar(app.secret_key)

        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("cadastro_usuario.html", usuario=dados)

        usuario.gravar_usuario()
        flash("Usuario cadastrado com sucesso.", "success")
        return redirect(url_for("novo_usuario"))
        
    except Exception as e:
        flash(f"Erro ao cadastrar usuario {e}", "danger")
        return render_template("cadastro_usuario.html", usuario=dados)



# ====== Buscando usuario ====== #
@app.route("/usuario/buscar/<int:id>", methods=["GET"])
def buscar_usuario(id):
    usuario = Usuario.buscar_usuario_por_id(id)
    if not usuario:
        flash("Usuario não encontrado.", "erro")
        return redirect(url_for("usuario"))
    #return render_template("formulario_usuario.html", usuario=usuario)
    return "Usuario encontrado"

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
        #return render_template("formulario_usuario.html", usuario=dados)
        return f"Erro: {erro}"

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
        #return render_template("formulario_usuario.html", usuario=dados)
        return f"Erro: {e}"

# ====== Excluindo usuarios ====== #
@app.route("/usuario/excluir/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    try:
        Usuario.deletar_usuario(id)
        flash("Usuario excluído com sucesso.", "sucesso")
        return "Usuario deletado", 200
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir usuario: {e}", "erro")
        return f"Erro ao excluir usaurio: {e}", 500
    return redirect(url_for("novo_usuario"))


# ====== Endpoints de cadstro de sensor ====== #


@app.route("/sensores")
def sensores():
    return render_template("sensores.html", sensores=Sensor.find_all(order_by="nome"))


@app.route("/sensor/novo")
def novo_sensor():
    return render_template("formulario_sensor.html", sensor=None)

# ====== Adicionado novos sensores ====== #
@app.route("/sensor/salvar", methods=["POST"])
def salvar_sensor():
    dados = get_sensor_form()
    sensor = Sensor(**dados)
    #erros = sensor.validar()

    '''
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("formulario_sensor.html", sensor=dados)'''

    try:
        sensor.gravar_sensor()
        flash("Sensor cadastrado com sucesso.", "sucesso")
        return redirect(url_for("sensores")), 200
    except Exception as e:
        flash(f"Erro ao cadastrar sensor: {e}", "erro")
        #return render_template("formulario_sensor.html", sensor=dados)
        return f"erro: {e}"

# ====== Editando dados de sensores ====== #
@app.route("/sensor/editar/<int:id>")
def editar_sensor(id):
    sensor = Sensor.buscar_sensor(id)
    if not sensor:
        flash("Sensor não encontrado.", "erro")
        return redirect(url_for("sensor"))
    return render_template("formulario_sensor.html", sensor=sensor)

# ====== Atualizando dados de sensores ====== #
@app.route("/sensor/atualizar/<int:id>", methods=["POST"])
def atualizar_sensor(id):
    dados = get_sensor_form()
    sensor = Sensor(**dados)
    #erros = sensor.validar()
    '''
    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("formulario_sensor.html", sensor=dados)'''

    try:
        if not Sensor.buscar_sensor(id):
            flash("Sensor não encontrado.", "erro")
            return redirect(url_for("sensores"))

        sensor.atualizar_sensor(id)
        flash("Sensor atualizado com sucesso.", "sucesso")
        return redirect(url_for("sensores")), 200
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar sensor: {e}", "erro")
        #return render_template("formulario_sensor.html", sensor=dados)
        return f"erro: {e}"

# ====== Excluindo sensores ====== #
@app.route("/sensor/excluir/<int:id>", methods=["DELETE"])
def excluir_sensor(id):
    try:
        Sensor.deletar_sensor(id)
        flash("Sensor excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
        return f"erro: {e}"
    except Exception as e:
        flash(f"Erro ao excluir sensor: {e}", "erro")
        return f"erro: {e}"
    return redirect(url_for("sensores")), 200


# ====== Endpoints da lista de compra ====== #


@app.route("/lista_compra")
def lista_compra():
    return render_template("lista_compra.html", lista_compra=Lista_compra.find_all(order_by="nome"))


@app.route("/lista_compra/novo")
def novo_lista_compra():
    return render_template("formulario_lista_compra.html", lista_compra=None)

# ====== Adicionado novos itens na lista de compra ====== #
@app.route("/lista_compra/salvar", methods=["POST"])
def salvar_lista_compra():
    dados = get_lista_compra_form()
    lista_compra = Lista_compra(**dados)
    erros = lista_compra.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("formulario_lista_compra.html", lista_compra=dados)

    try:
        lista_compra.insert()
        flash("Lista compra feita com sucesso.", "sucesso")
        return redirect(url_for("lista_compra"))
    except Exception as e:
        flash(f"Erro ao criar lista de compras: {e}", "erro")
        return render_template("formulario_lista_compra.html", lista_compra=dados)

# ====== Excluindo itens da lista de compra ======#
@app.route("/lista_compra/excluir/<int:id>")
def excluir_lista_compra(id):
    try:
        Lista_compra.safe_delete(id)
        flash("Lista de compra excluíds com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir lista de compra: {e}", "erro")
    return redirect(url_for("lista_compra"))


# ====== Endpoints de pesquisas ====== #

# ====== Editando pesquisa ====== #
@app.route("/pesquisa_item/editar/<int:id>")
def editar_pesquisa_item(id):
    pesquisa_item = pesquisa_item.find_by_id(id)
    if not pesquisa_item:
        flash("Item não encontrado.", "erro")
        return redirect(url_for("pesquisa_item"))
    return render_template("formulario_pesquisa_item.html", pesquisa_item=pesquisa_item)


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
    erros = login.login_validar(app.secret_key)

    if erros:
        for erro in erros:
            flash(erro, "danger")
        return render_template("login.html", login=dados)

    try:
        usuario = login.autenticar_login()

        if not usuario:
            flash("Usuário não encontrado", "danger")
            return render_template("login.html", login=dados)


        flash("Login feito com sucesso.", "success")
        return redirect(url_for("novo_login"))

    except Exception as e:
        flash(f"Erro ao fazer login", "danger")
        return render_template("login.html", login=dados)


# ====== Executar codigo ======#
if __name__ == "__main__":
    app.run(debug=True)