from flask import jsonify, request

# 1. Função de banco isolada (fora do endpoint)
def buscar_nome_produto(produto_id):
    conexao = Database.connect()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Correção: Adicionado o "where" correto usando o parâmetro %s
        query = """
            SELECT p.produto_nome, p.produto_categoria, e.estoque_quantidade 
            FROM produto p 
            JOIN estoque e ON e.produto_produto_id = p.produto_id
            WHERE p.produto_id = %s;
        """
        cursor.execute(query, (produto_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return None
        return resultado
    finally:
        cursor.close()
        conexao.close()

# 2. Endpoint Flask corrigido
@app.route("/relatorio")
def buscar_estoque():
    # Captura o ID enviado na URL (Ex: /relatorio?id=5)
    produto_id = request.args.get('id')
    
    if not produto_id:
        return jsonify({"erro": "O parâmetro 'id' é obrigatório."}), 400

    dados = buscar_nome_produto(produto_id)
    print("dados banco:", dados)

    if not dados:
        return jsonify({"erro": "Estoque não encontrado para esse produto."}), 404

    # Retorna os dados do banco em formato JSON
    return jsonify(dados), 200
