# ====== Importação de bibliotecas ====== #
#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash
from models.produto import Produto
from models.sensor import Sensor
from models.usuario import Usuario
from models.lista_compra import Lista_compra
from models.login import Login
from models.fornecedor import Fornecedor
from models.animal import Animal
from models.pedido_entrada import Pedido_entrada
from models.gerenciamento_perfil import GerenciametoPerfil


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

# ====== Pegando os dados para a lista de compra ======#
def get_lista_compra_form():
        return{
        "nome_produto": request.form.get("nome_produto", "").strip(),
        "produto_id": to_int(request.form.get("produto_id")),
        "quantidade": to_int(request.form.get("quantidade")),
        "custo_compra": to_float(request.form.get("custo_compra")),
    }

def get_gerenciar_perfil_form():
        return{
        "nome": request.form.get("nome", "").strip(),
        "email": to_int(request.form.get("email", "")),
        "cargo": to_int(request.form.get("cargo", "")),
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
    return render_template("landingpage.html")

@app.route("/inicial")
def inicial():
    return render_template("base.html")

# ====== Endpoints para o cadastro de produtos ====== #

# ===== Rotas iniciais tela de produto ====== #
@app.route("/produtos")
def produtos():
    return render_template("cadastro_produto.html")

@app.route("/produto/novo")
def novo_produto():
    return render_template("cadastro_produto.html", produto=None)


# ====== Cadaastrando novos produtos ====== #
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
        return render_template("cadastro_produto.html", produto=dados)



# ====== Editando cadastros de produtos ======#
@app.route("/produto/atualizar/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar_produto()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        dados["id"] = id
        return render_template("cadastro_produto.html", produto=dados)

    try:
        if not Produto.buscar_por_id(id):
            flash("Produto não encontrado.", "danger")
            return redirect(url_for("produtos"))

        produto.atualizar_produto(id)
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("produtos"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar produto: {e}", "danger")
        return render_template("cadastro_produto.html", produto=dados)


# ====== Deletando produtos ====== #
@app.route("/produto/excluir/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    try:
        Produto.deletar_produto(id)
        flash("Produto excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
        return render_template("cadastro_produto.html")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "danger")
        return render_template("cadastro_produto.html")
    return redirect(url_for("produtos"))


# ====== Endpoint de movimentação de produtos ======#

@app.route("/movimentacoes")
def movimentacoes():
    return render_template("movimentacoes.html")


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
    return render_template("cadastro_usuario.html", usuario=usuario)

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

# ====== Excluindo usuarios ====== #
@app.route("/usuario/excluir/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    try:
        Usuario.deletar_usuario(id)
        flash("Usuario excluído com sucesso.", "sucesso")
        return "Usuario deletado"
    except ValueError as e:
        flash(str(e), "erro")
        return f"Erro ao excluir usaurio: {e}"
    except Exception as e:
        flash(f"Erro ao excluir usuario: {e}", "erro")
        return f"Erro ao excluir usaurio: {e}"
    return redirect(url_for("novo_usuario"))


# ====== Endpoints de cadstro de sensor ====== #


@app.route("/sensores")
def sensor():
    return render_template("cadastro_sensor.html")


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
        return render_template("cadastro_sensor.html", usuario=dados)
    
    try:
        sensor.gravar_sensor()
        flash("Sensor cadastrado com sucesso.", "success")
        return redirect(url_for("novo_sensor"))
    except Exception as e:
        flash(f"Erro ao cadastrar sensor: {e}", "danger")
        return render_template("Cadastro_sensor.html", sensor=dados)

# ====== Editando dados de sensores ====== #
@app.route("/sensor/editar/<int:id>")
def editar_sensor(id):
    sensor = Sensor.buscar_sensor(id)
    if not sensor:
        flash("Sensor não encontrado.", "danger")
        return redirect(url_for("successs"))
    return render_template("cadastro_sensor.html", sensor=sensor)

# ====== Atualizando dados de sensores ====== #
@app.route("/sensor/atualizar/<int:id>", methods=["POST"])
def atualizar_sensor(id):
    dados = get_sensor_form()
    sensor = Sensor(**dados)
    erros = sensor.validar()

    if erros:
        for erro in erros:
            flash(erro, "danger")
        dados["id"] = id
        return render_template("cadastro_sensor.html", sensor=dados)

    try:
        if not Sensor.buscar_sensor(id):
            flash("Sensor não encontrado.", "danger")
            return redirect(url_for("sensor"))

        sensor.atualizar_sensor(id)
        flash("Sensor atualizado com sucesso.", "success")
        return redirect(url_for("sensor")), 200
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar sensor: {e}", "danger")
        return render_template("cadastro_sensor.html", sensor=dados)

# ====== Excluindo sensores ====== #
@app.route("/sensor/excluir/<int:id>", methods=["DELETE"])
def excluir_sensor(id):
    try:
        Sensor.deletar_sensor(id)
        flash("Sensor excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
        return f"erro: {e}"
    except Exception as e:
        flash(f"Erro ao excluir sensor: {e}", "danger")
        return f"erro: {e}"
    return redirect(url_for("sensor"))


# ====== Endpoints da lista de compra ====== #


@app.route("/lista_compra")
def lista_compra():
    return render_template("lista_compra.html")


@app.route("/lista_compra/novo")
def novo_lista_compra():
    return render_template("lista_compra.html", lista_compra=None)

# ====== Adicionado novos itens na lista de compra ====== #
@app.route("/lista_compra/salvar", methods=["POST"])
def salvar_lista_compra():
    dados = get_lista_compra_form()
    lista_compra = Lista_compra(**dados)
    erros = lista_compra.validar()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("lista_compra.html", lista_compra=dados)

    try:
        lista_compra.insert()
        flash("Lista compra feita com sucesso.", "success")
        return redirect(url_for("lista_compra"))
    except Exception as e:
        flash(f"Erro ao criar lista de compras: {e}", "danger")
        return render_template("lista_compra.html", lista_compra=dados)

# ====== Excluindo itens da lista de compra ======#
@app.route("/lista_compra/excluir/<int:id>")
def excluir_lista_compra(id):
    try:
        Lista_compra.safe_delete(id)
        flash("Lista de compra excluíds com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir lista de compra: {e}", "danger")
    return redirect(url_for("lista_compra"))


# ====== Endpoints de pesquisas ====== #

# ====== Editando pesquisa ====== #
@app.route("/pesquisa_item/editar/<int:id>")
def editar_pesquisa_item(id):
    pesquisa_item = pesquisa_item.find_by_id(id)
    if not pesquisa_item:
        flash("Item não encontrado.", "danger")
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
    erros = login.validar_login(app.secret_key)

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
        flash(f"Erro ao fazer login {e}", "danger")
        return render_template("login.html", login=dados)

#endpoint animal
@app.route("/animal")
def animal():
    return render_template("cadastro_animais.html")

@app.route("/animal/novo", methods=['GET', 'POST'])
def novo_animal():
    return render_template("cadastro_animais.html", usuario=None)


@app.route("/animal/salvar", methods=["POST"])
def salvar_animal():
    try:
        dados = get_animal_form()
        animal = Animal(**dados)
        erros = animal.validar()

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



@app.route("/animal/buscar/<int:id>", methods=["GET"])
def buscar_animal(id):
    animal = Animal.buscar_animal_por_id(id)
    if not animal:
        flash("Animal não encontrado.", "erro")
        return redirect(url_for("animal"))
    return render_template("cadastro_usuario.html", animal=animal)


# Endpoints fornecedor

@app.route("/fornecedor")
def fornecedor():
    return render_template("cadastro_fornecedor.html")

@app.route("/fornecedor/novo")
def fornecedor_novo():
    return render_template("cadastro_fornecedor.html")

@app.route("/fornecedor/salvar", methods=["POST"])
def gravar_fornecedor():
    dados = get_gerenciar_perfil_form()
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
        return render_template("cadastrar_fornecedor.html", login=dados)
    
# Endpoint gerenciamento de perfil

@app.route("/gerenciar_perfil", methods=["GET"])
def gerenciar_perfil():
    return render_template("gerenciamento_perfil.html")

@app.route("/gerenciar_perfil/atualizar", methods=["GET"])
def gerenciar_perfil_atualizar():
    return render_template("gerenciamento_perfil.html")

@app.route("/gerenciar_perfil/salvar", methods=["GET", "POST"])
def gerenciar_perfil_atualizar_salvar():

    dados = get_fornecedor_form()
    atualizar = GerenciametoPerfil(**dados)
    erros = atualizar.validar_fornecedor()

    try:

        if erros:
            flash(erros, "danger")
            return render_template("gerenciar_perfil.html")

        atualizar.atualizar_usuario()

        flash("Dados atualizados.", "success")
        return redirect(url_for(""))

    except Exception as e:
        flash(f"Erro ao atualizar dados", "danger")
        return render_template("cadastrar_fornecedor.html", login=dados)


# Endpoint informação produto

@app.route("/informacao_produto")
def inforcao_produto():
    return render_template("informacao_produto.html")

# Endpoint entrada produto

@app.route("/produto_entrada")
def produto_entrada():
    return render_template("pedido_entrada.html")

# Endpoint saída produto

@app.route("/produto_saida")
def produto_saida():
    return render_template("pedido_saida.html")




# ====== Executar codigo ======#
if __name__ == "__main__":
    app.run(debug=True)