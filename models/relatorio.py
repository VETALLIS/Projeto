from core.conectar import Database


def buscar_estoque_db(nome=None, categoria=None, quantidade=None):

    conexao = None
    cursor = None

    try:
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        #Seleciona os dados do produto e a quantidade do estoque
        query = """
            SELECT
                p.produto_id,
                p.produto_nome,
                p.produto_categoria,
                e.estoque_quantidade

            FROM produto p

            INNER JOIN estoque e
                ON e.produto_produto_id = p.produto_id

            WHERE 1 = 1
        """

        # Lista dos valores que substituirão os %s da query, na ordem em que aparecem
        parametros = []

        if nome:
            # LIKE permite busca parcial 
            query += """
                AND p.produto_nome LIKE %s
            """

            parametros.append(
                f"%{nome}%"
            )



        if categoria:
            #Comparação exata
            query += """
                AND p.produto_categoria = %s
            """

            parametros.append(
                categoria
            )


        # ==========================================
        # FILTRO QUANTIDADE
        # ==========================================

        if quantidade is not None:
            # Adiciona na busca: "quantidade exatamente igual a essa"
            query += """
                AND e.estoque_quantidade = %s
            """

            parametros.append(
                quantidade
            )


     # Coloca o resultado em ordem alfabética (A até Z)
        query += """
            ORDER BY p.produto_nome ASC
        """

    # Manda o comando para o banco.
        cursor.execute(
            query,
            tuple(parametros)
        )



    # Pega todas as linhas retornadas como uma lista de dicionários
        produtos = cursor.fetchall()



        return produtos #Retorna o que foi encontrado


    except Exception as erro:


        raise


    finally:

        if cursor is not None:

            cursor.close() #fecha o cursor se estiver aberto


        if conexao is not None:

            conexao.close() #fecha a conexao se estiver aberta
