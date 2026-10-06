from core.conectar import Database # Importo a classe Database, que é a que faz a conexão com o banco de dados

class Crud_base:  #classe base do crud, as outras herdarão dela.
    tabela = ""  # nome da tabela no banco 
    fields = [] # lista com as colunas que vão ser gravadas/atualizadas
    pk = "id" # nome da chave primária, id

    @classmethod
    def buscar_tudo(cls, order_by): 
        conexao = Database.connect() # abre a conexão com o banco
        cursor = conexao.cursor(dictionary=True)  # dictionary=True faz o resultado vir como dicionário

        try:
            sql = f"SELECT * FROM {cls.tabela} ORDER BY {order_by}" # monto o SELECT usando o nome da tabela da classe e a coluna de ordenação
            cursor.execute(sql)
            return cursor.fetchall() # fetchall pega TODAS as linhas que o select trouxe
        finally:
            cursor.close()
            conexao.close()
            # o finally sempre roda, dando erro ou não
            #fecha o cursor e a conexão pra não ficar nada aberto

    def gravar(self):  # método de instância (usa o self), ou seja, precisa de um objeto já criado
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            colunas = ", ".join(self.fields)  # junta os nomes dos campos separados por vírgula: "nome, categoria, preco"
            marcadores = ", ".join(["%s"] * len(self.fields))  # cria um %s pra cada campo: "%s, %s, %s"
            valores = tuple(getattr(self, campo) for campo in self.fields)# pega o valor de cada campo do objeto usando getattr
            # (getattr(self, "nome") é igual a self.nome, só que dinâmico)

            sql = f"INSERT INTO {self.tabela} ({colunas}) VALUES ({marcadores})"

            cursor.execute(sql, valores)# salva no banco
            conexao.commit()
            return cursor.lastrowid # lastrowid devolve o id do registro que acabou de ser inserido
        except Exception:
            conexao.rollback() # se der algum erro, desfaz tudo que foi feito (rollback)
            raise #tenta ver o que deu errado
        finally:
            cursor.close()
            conexao.close()

    def atualizar(self, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try: # apaga só o registro que tem aquele id
            campos = ", ".join([f"{campo} = %s" for campo in self.fields]) # monta a parte do SET
            valores = tuple(getattr(self, campo) for campo in self.fields) + (id,)# os valores dos campos + o id no final 
            sql = f"UPDATE {self.tabela} SET {campos} WHERE {self.pk} = %s"  
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount # rowcount diz quantas linhas foram alteradas (0 = não achou o id
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def deletar(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = f"DELETE FROM {cls.tabela} WHERE {cls.pk} = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_por_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"SELECT * FROM {cls.tabela} WHERE {cls.pk} = %s"
            cursor.execute(sql, (id,))
            return cursor.fetchone()  # fetchone pega só uma linha
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_para_login(cls, email):  # busca o usuário pelo email pra fazer o login
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE usuario_email = %s "
            cursor.execute(sql, (email,))
            resultados = cursor.fetchall() 
            return resultados[0] if resultados else None # se encontrou alguém, retorna o primeiro; se não, retorna None
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_email(cls, email):  # verifica se um email já está cadastrado 
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE LOWER(TRIM(usuario_email)) = LOWER(TRIM(%s))"   # LOWER deixa tudo minúsculo e TRIM tira os espaços 
            cursor.execute(sql, (email,))
            resultado = cursor.fetchone()

            # Retorna True se o usuário foi encontrado, ou False se não existir
            if resultado:
                return True
            else:
                return False

        finally:
            cursor.close()
            conexao.close()


    @staticmethod
    def buscar_categoria_produto(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute("select p.produto_nome, p.produto_categoria, e.estoque_quantidade from produto p join estoque e where e.produto_produto_id = p.produto_id;", (id,))
            resultado = cursor.fetchone() 
            if not resultado: # se não achou envia uma mensagem de erro
                raise ValueError("Estoque não encontrado para esse produto.")
            return resultado["estoque_id"]
        finally:
            cursor.close()
            conexao.close()



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