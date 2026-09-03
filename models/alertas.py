# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database
from datetime import date

# ===== Cria a classe Alertas ===#
class Alertas(Crud_base):

    # Define a tabela e os campos do banco
    tabela = "notificacao"
    pk = "notificacao_id"
    fields = ["notificacao_status","notificacao_data" ]

    # Define os atributos 
    def __init__(self,notificacao_data, notificacao_status):
        self.notificacao_status = notificacao_status
        self.notificacao_data = notificacao_data

    def deletar_alerta(self, id):
        alerta = self.buscar_por_id(id)

        if not alerta:
            raise ValueError("Alerta não encontrado")

        self.deletar(id)
        return "Alerta deletado com sucesso!"
    
    @staticmethod
    def registrar_notificacao(cursor, descricao):
        sql_check = """
        SELECT notificacao_id FROM notificacao
        WHERE notificacao_descricao = %s AND notificacao_status = 'pendente'
        """
        cursor.execute(sql_check, (descricao,))
        if cursor.fetchone():
            return  # já existe, não duplica

        sql_insert = """
        INSERT INTO notificacao (notificacao_status, notificacao_data, notificacao_descricao)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql_insert, ("pendente", date.today(), descricao))

    @staticmethod    
    def contar_baixo_estoque():
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT 
                p.produto_id, p.produto_nome, p.produto_categoria,
                e.estoque_quantidade
            FROM produto p
            INNER JOIN estoque e
                ON e.produto_produto_id = p.produto_id
            WHERE e.estoque_quantidade < 5
            """
            cursor.execute(sql)
            baixo_estoque = cursor.fetchall()

            for item in baixo_estoque:
                descricao = f"Estoque baixo: {item['produto_nome']} ({item['estoque_quantidade']} unidades restantes)"
                Alertas.registrar_notificacao(cursor, descricao)
            conexao.commit()

            return baixo_estoque
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def contar_vencidos():
        conexao =  Database.connect()
        cursor =  conexao.cursor()

        try:
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True)

            sql = """   
            SELECT 
            p.produto_id, p.produto_nome, p.produto_categoria,
            ipe.item_pedido_entrada_validade
            FROM produto p
            INNER JOIN item_pedido_entrada ipe
            ON p.produto_id = ipe.produto_produto_id
            WHERE (
                STR_TO_DATE(ipe.item_pedido_entrada_validade, '%Y-%m-%d') < CURDATE()
                OR
                STR_TO_DATE(ipe.item_pedido_entrada_validade, '%d/%m/%Y') < CURDATE()
            )
            """

            cursor.execute(sql)
            vencidos = cursor.fetchall()
            for item in vencidos:
                descricao = (
                    f"Produto vencido: {item['produto_nome']} "
                    f"(validade {item['item_pedido_entrada_validade']})"
                )
                Alertas.registrar_notificacao(cursor, descricao)

            conexao.commit()
            return vencidos
        finally:
            cursor.close()
            conexao.close()
    
    @staticmethod
    def contar_data_relativa():
        conexao =  Database.connect()
        cursor =  conexao.cursor()

        try:
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT 
                p.produto_id, 
                p.produto_nome, 
                p.produto_categoria,
                ipe.item_pedido_entrada_validade
                FROM produto p
                INNER JOIN item_pedido_entrada ipe
                ON ipe.produto_produto_id = p.produto_id
                WHERE (
                STR_TO_DATE(ipe.item_pedido_entrada_validade, '%Y-%m-%d') 
                BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
                OR
                STR_TO_DATE(ipe.item_pedido_entrada_validade, '%d/%m/%Y') 
                BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
                )
            """

            cursor.execute(sql)
            perto_vencimento = cursor.fetchall()
            for item in perto_vencimento:
                descricao = (
                    f"Vence em breve: {item['produto_nome']} "
                    f"(validade {item['item_pedido_entrada_validade']})"
                )
                Alertas.registrar_notificacao(cursor, descricao)

            conexao.commit()
            return perto_vencimento
        finally:
            cursor.close()
            conexao.close()
        
    @staticmethod
    def buscar_pendentes():
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT notificacao_id, notificacao_status, notificacao_data, notificacao_descricao
            FROM notificacao
            WHERE notificacao_status = 'pendente'
            ORDER BY notificacao_data DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    
