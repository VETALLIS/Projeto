# ====== Importação de bibliotecas ====== #
# Importa o Flask e os utilitários necessários para rotas, templates, requisições e redirecionamentos
from flask import Flask, render_template, request, redirect, url_for, flash

# Importa os modelos responsáveis pela lógica de negócio e acesso ao banco de dados
from models.produto import Produto
from models.movimentacao import Movimentacao
from models.sensor import Sensor
from models.usuario import Usuario
from models.lista_compra import Lista_compra
from models.login import Login

# Instancia a aplicação Flask
app = Flask(__name__)

# Chave secreta usada na validação de sessão e tokens
app.secret_key = "25713|TFZjE1B6p5Q21TSHCOs9Xre7GB9Vwc0P"


# ====== converter inteiro ====== #
# Tenta converter um valor para inteiro; retorna o valor padrão em caso de falha
def to_int(value, default=0): 
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# ====== converter decimal ====== #
# Tenta converter um valor para float; retorna o valor padrão em caso de falha
def to_float(value, default=0.0): 
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ====== Pegando os dados do Front End ====== #

# ====== Pegando os dados de produto ====== #
# Extrai e sanitiza os campos do formulário de produto enviados via POST
def get_produto_form(): 
    return {
        "produto_nome": request.form.get("nome", "").strip(),
        "produto_descricao": request.form.get("descricao", "").strip(),
        "produto_categoria": request.form.get("categoria", "").strip(),
        "usuario_usuario_id": request.form.get("usuario_usuario_id", "").strip()
    }


# ====== Pegando os dados de pedidos ====== #
# Extrai e sanitiza os campos do formulário de movimentação/pedido enviados via POST
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
# Extrai e sanitiza os campos do formulário de cadastro de usuário
def get_usuario_form():
    return{
        "usuario_nome": request.form.get("nome", "").strip(),
        "usuario_email": request.form.get("email", "").strip(),
        "usuario_cpf":request.form.get("cpf", "").strip(),
        "usuario_senha":request.form.get("senha", "").strip(),
        "usuario_cargo": request.form.get("cargo", "").strip()
    }

# ====== Pegando os dados para o login ====== #
# Extrai e sanitiza os campos do formulário de login
def get_login_form():
    return{
        "login_email": request.form.get("email", "").strip(),
        "login_senha":request.form.get("senha", "").strip(),
    }

# ====== Pegando os dados para o cadastro de sensores ====== #
# Extrai e sanitiza os campos do formulário de cadastro de sensor
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
# Extrai e sanitiza os campos do formulário de lista de compra
def get_lista_compra_form():
        return{
        "nome_produto": request.form.get("nome_produto", "").strip(),
        "produto_id": to_int(request.form.get("produto_id")),
        "quantidade": to_int(request.form.get("quantidade")),
        "custo_compra": to_float(request.form.get("custo_compra")),
    }

# ====== Pegando os dados para a pesquisa ====== #
# Extrai o nome do produto informado no campo de pesquisa
def get_pesquisa_item_form():
        return{
        "nome_produto": request.form.get("nome_produto", "").strip(),
    }

# ========= Definição das rotas e dos endpoints ========= #

# ====== Rota de teste ====== #
# Rota raiz; exibe a landing page da aplicação
@app.route("/")
def index():
    #produtos_baixo = Produto.low_stock()
    return render_template("landingpage.html")


# ====== Endpoints para o cadastro de produtos ====== #

# ===== Buscando produtos ====== #
# Lista todos os produtos ordenados pelo nome
@app.route("/produtos", methods=["GET"])
def produtos():
    return render_template("produtos.html", produtos=Produto.buscar_todo_produto(order_by="produto_nome"))


# Exibe o formulário de cadastro de novo produto
@app.route("/produto/novo")
def novo_produto():
    return render_template("formulario_produto.html", produto=None)

# ====== Cadastrando novos produtos ====== #
# Recebe os dados do formulário, valida e persiste um novo produto no banco
@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar()

    # Retorna os erros de validação caso existam
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
# Recebe os dados atualizados, valida e atualiza o produto identificado pelo id
@app.route("/produto/atualizar/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validar()

    if erros:        
        return f"Erro: {erros}"

    try:
        # Verifica se o produto existe antes de tentar atualizar
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
# Remove o produto identificado pelo id; trata erros de valor e erros genéricos separadamente
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


# ====== Endpoint de movimentação de produtos ======#
# Lista todas as movimentações com os dados do produto associado
@app.route("/movimentacoes")
def movimentacoes():
    return render_template("movimentacoes.html", movimentacoes=Movimentacao.find_all_with_product())


# ====== Endpoints de cadastro de novos usuarios ======#

# Exibe o formulário de cadastro de novo usuário
@app.route("/usuario/novo", methods=['GET', 'POST'])
def novo_usuario():
    return render_template("cadastro.html", usuario=None)

# ====== Adicionado novo usuario ====== #
# Recebe os dados do formulário, valida e persiste um novo usuário no banco
@app.route("/usuario/salvar", methods=["POST"])
def salvar_usuario():
    try:
        dados = get_usuario_form()
        usuario = Usuario(**dados)
        erros = usuario.validar(app.secret_key)

        # Retorna ao formulário exibindo os erros caso a validação falhe
        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("cadastro.html", usuario=dados)

        usuario.gravar_usuario()
        flash("Usuario cadastrado com sucesso.", "success")
        return redirect(url_for("novo_usuario"))
        
    except Exception as e:
        flash(f"Erro ao cadastrar usuario {e}", "danger")
        return render_template("cadastro.html", usuario=dados)



# ====== Buscando usuario ====== #
# Busca um usuário pelo id; redireciona com mensagem de erro se não encontrado
@app.route("/usuario/buscar/<int:id>", methods=["GET"])
def buscar_usuario(id):
    usuario = Usuario.buscar_usuario_por_id(id)
    if not usuario:
        flash("Usuario não encontrado.", "erro")
        return redirect(url_for("usuario"))
    #return render_template("formulario_usuario.html", usuario=usuario)
    return "Usuario encontrado"

# ====== Atualizando dados de usuario ====== #
# Recebe os dados atualizados, valida e atualiza o usuário identificado pelo id
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
        # Verifica se o usuário existe antes de tentar atualizar
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
# Remove o usuário identificado pelo id
@app.route("/usuario/excluir/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    try:
        Usuario.deletar_usuario(id)
        flash("Usuario excluído com sucesso.", "sucesso")
        return "Usuario deletado"
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir usuario: {e}", "erro")
        return f"Erro ao excluir usaurio: {e}"
    return redirect(url_for("novo_usuario"))


# ====== Endpoints de cadastro de sensor ====== #

# Lista todos os sensores ordenados pelo nome
@app.route("/sensores")
def sensores():
    return render_template("sensores.html", sensores=Sensor.find_all(order_by="nome"))


# Exibe o formulário de cadastro de novo sensor
@app.route("/sensor/novo")
def novo_sensor():
    return render_template("formulario_sensor.html", sensor=None)

# ====== Adicionado novos sensores ====== #
# Recebe os dados do formulário e persiste um novo sensor no banco
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
# Busca o sensor pelo id e exibe o formulário de edição; redireciona se não encontrado
@app.route("/sensor/editar/<int:id>")
def editar_sensor(id):
    sensor = Sensor.buscar_sensor(id)
    if not sensor:
        flash("Sensor não encontrado.", "erro")
        return redirect(url_for("sensor"))
    return render_template("formulario_sensor.html", sensor=sensor)

# ====== Atualizando dados de sensores ====== #
# Recebe os dados atualizados e persiste as alterações do sensor identificado pelo id
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
        # Verifica se o sensor existe antes de tentar atualizar
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
# Remove o sensor identificado pelo id; trata erros de valor e erros genéricos separadamente
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
    return redirect(url_for("sensores"))


# ====== Endpoints da lista de compra ====== #

# Lista todos os itens da lista de compra ordenados pelo nome
@app.route("/lista_compra")
def lista_compra():
    return render_template("lista_compra.html", lista_compra=Lista_compra.find_all(order_by="nome"))


# Exibe o formulário de adição de novo item na lista de compra
@app.route("/lista_compra/novo")
def novo_lista_compra():
    return render_template("formulario_lista_compra.html", lista_compra=None)

# ====== Adicionado novos itens na lista de compra ====== #
# Recebe os dados do formulário, valida e insere um novo item na lista de compra
@app.route("/lista_compra/salvar", methods=["POST"])
def salvar_lista_compra():
    dados = get_lista_compra_form()
    lista_compra = Lista_compra(**dados)
    erros = lista_compra.validate()

    # Retorna ao formulário exibindo os erros caso a validação falhe
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
# Remove o item da lista de compra identificado pelo id
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
# Busca um item de pesquisa pelo id e exibe o formulário de edição; redireciona se não encontrado
@app.route("/pesquisa_item/editar/<int:id>")
def editar_pesquisa_item(id):
    pesquisa_item = pesquisa_item.find_by_id(id)
    if not pesquisa_item:
        flash("Item não encontrado.", "erro")
        return redirect(url_for("pesquisa_item"))
    return render_template("formulario_pesquisa_item.html", pesquisa_item=pesquisa_item)


# ====== Endpoints para o login ======#

# Exibe a página de login; aceita um parametro de status opcional via query string
@app.route("/login/novo", methods=["GET", "POST"])
def novo_login():
    status = request.args.get("status")
    return render_template("login.html", status=status)


# ====== Registrar login ======#
# Recebe as credenciais, valida o formato e autentica o usuário no sistema
@app.route("/login/salvar", methods=["POST"])
def salvar_login():
    dados = get_login_form()
    login = Login(**dados)
    erros = login.login_validar(app.secret_key)

    # Retorna ao formulário exibindo os erros caso a validação falhe
    if erros:
        for erro in erros:
            flash(erro, "danger")
        return render_template("login.html", login=dados)

    try:
        usuario = login.autenticar_login()

        # Informa que o usuário não foi encontrado caso a autenticação não retorne resultado
        if not usuario:
            flash("Usuário não encontrado", "danger")
            return render_template("login.html", login=dados)

        flash("Login feito com sucesso.", "success")
        return redirect(url_for("novo_login"))

    except Exception as e:
        flash(f"Erro ao fazer login", "danger")
        return render_template("login.html", login=dados)


# ====== Executar codigo ======#
# Inicia o servidor Flask em modo de depuração quando executado diretamente
if __name__ == "__main__":
    app.run(debug=True)