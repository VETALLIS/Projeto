# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database

# ===== Cria a classe Alertas ===#
class Alertas(Crud_base):

    # Define a tabela e os campos do banco
    tabela = "notificacao"
    pk = "notificacao_id"
    fields = ["notificacao_status","notificacao_data", ]

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

        
    def contar_baixo_estoque():
        conexao =  Database.connect()
        cursor =  conexao.cursor()

        try:
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT 
                    p.produto_id, p.produto_nome, p.produto_categoria,
                FROM produto p
                INNER JOIN item_pedido_entrada ipe
                    ON ipe.produto_id = p.produto_produto_id
                WHERE e.estoque_quantidade < 5
            """

            cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados
        finally:
            cursor.close()
            conexao.close()

    def contar_vencidos():
        conexao =  Database.connect()
        cursor =  conexao.cursor()

        try:
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT 
                    p.produto_id, p.produto_nome, p.produto_categoria,ipe.item_pedido_entrada_validade
                FROM produto p
                INNER JOIN estoque e
                    ON e.produto_id = p.produto_produto_id
                WHERE (
                        STR_TO_DATE(ipe.item_pedido_entrada_validade, '%Y-%m-%d') < CURDATE()
                        OR
                        STR_TO_DATE(ipe.item_pedido_entrada_validade, '%d/%m/%Y') < CURDATE()
                )
            """

            cursor.execute(sql)
            vencidos = cursor.fetchall()
            return vencidos
        finally:
            cursor.close()
            conexao.close()
    
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
            return perto_vencimento
        finally:
            cursor.close()
            conexao.close()
