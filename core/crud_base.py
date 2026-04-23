from core.conectar import Database

class Crud_base:
    tabela = ""
    fields = []
    pk = "id"

    @classmethod
    def buscar_tudo(cls, order_by="id"):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"SELECT * FROM {cls.tabela} ORDER BY {order_by}"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    def gravar(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            colunas = ", ".join(self.fields)
            marcadores = ", ".join(["%s"] * len(self.fields))
            valores = tuple(getattr(self, campo) for campo in self.fields)

            sql = f"INSERT INTO {self.tabela} ({colunas}) VALUES ({marcadores})"

            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    def atualizar(self, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            campos = ", ".join([f"{campo} = %s" for campo in self.fields])
            valores = tuple(getattr(self, campo) for campo in self.fields) + (id,)
            sql = f"UPDATE {self.tabela} SET {campos} WHERE {self.pk} = %s"
            print(f"SQL: {sql}")        # ← adicione isso
            print(f"PK: {self.pk}")   
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount
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
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_para_login(cls, email):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE usuario_email = %s "
            cursor.execute(sql, (email,))
            resultados = cursor.fetchall()
            return resultados[0] if resultados else None
        finally:
            cursor.close()
            conexao.close()