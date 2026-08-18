from core.conectar import Database


def buscar_estoque_db(nome=None, categoria=None, quantidade=None):

    conexao = None
    cursor = None

    try:
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
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


        parametros = []

        if nome:

            query += """
                AND p.produto_nome LIKE %s
            """

            parametros.append(
                f"%{nome}%"
            )



        if categoria:

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

            query += """
                AND e.estoque_quantidade = %s
            """

            parametros.append(
                quantidade
            )



        query += """
            ORDER BY p.produto_nome ASC
        """


        cursor.execute(
            query,
            tuple(parametros)
        )




        produtos = cursor.fetchall()



        return produtos


    except Exception as erro:


        raise


    finally:

        if cursor is not None:

            cursor.close()


        if conexao is not None:

            conexao.close()