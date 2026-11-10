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
    fields = ["notificacao_status","notificacao_data", "notificacao_descricao" ]


    
    def deletar_alerta(self, id): #def para deletar notificação de alerta
        alerta = self.buscar_por_id(id) #verifica se tem alerta

        if not alerta:
            raise ValueError("Alerta não encontrado") #se não há alerta, retorna essa mensagem

        self.deletar(id)
        return "Alerta deletado com sucesso!" #se o alerta for deltado, retorna essa mensagem

    @staticmethod
    def limpar_notificacoes_antigas(dias=7): 
        """
        Deleta automaticamente as notificações do banco com mais de 7 dias.
        """
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            # Query usando funções nativas do MySQL (DATEDIFF ou DATE_SUB)
            sql = """
            DELETE FROM notificacao 
            WHERE notificacao_data < DATE_SUB(CURDATE(), INTERVAL %s DAY)
            """
            cursor.execute(sql, (dias,))
            conexao.commit()
            
            # Retorna a quantidade de registros deletados
            return cursor.rowcount  
        finally: #fechamento de cursor e conexão
            cursor.close()
            conexao.close()
    
    @staticmethod
    def registrar_notificacao(cursor, descricao): #verifica se já existe uma notificação pendente igual
        sql_check = """
        SELECT notificacao_id FROM notificacao
        WHERE notificacao_descricao = %s AND notificacao_status = 'pendente'
        """
        cursor.execute(sql_check, (descricao,))
        if cursor.fetchone():
            return  # já existe, não duplica

        #se não existe, cria a notificação como "pendente" com a data de hoje
        sql_insert = """
        INSERT INTO notificacao (notificacao_status, notificacao_data, notificacao_descricao)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql_insert, ("pendente", date.today(), descricao))

    @staticmethod    
    def contar_baixo_estoque():
        conexao = Database.connect() #abre conexão com o banco
        cursor = conexao.cursor(dictionary=True) #linhas voltam como dicionário
        try:#busca produtos com estoque entre 1 e 9 unidades
            sql = """
            SELECT 
                p.produto_id, p.produto_nome, p.produto_categoria,
                e.estoque_quantidade
            FROM produto p
            INNER JOIN estoque e
                ON e.produto_produto_id = p.produto_id
            WHERE e.estoque_quantidade < 20 and e.estoque_quantidade >= 1
            """
            cursor.execute(sql)
            baixo_estoque = cursor.fetchall()

            for item in baixo_estoque:
                descricao = f"Estoque baixo: {item['produto_nome']} ({item['estoque_quantidade']} unidades restantes)"
                Alertas.registrar_notificacao(cursor, descricao)
            conexao.commit()

            return baixo_estoque #retorna os q estão abaixo de estoque
        finally: #fechamento de cursor e conexão
            cursor.close()
            conexao.close()

    @staticmethod    
    def contar_sem_estoque():
        conexao = Database.connect() #abre conexão com o banco
        cursor = conexao.cursor(dictionary=True) #linhas voltam como dicionário
        try:#busca produtos com estoque entre 1 e 9 unidades
            sql = """
            SELECT 
                p.produto_id, p.produto_nome, p.produto_categoria,
                e.estoque_quantidade
            FROM produto p
            INNER JOIN estoque e
                ON e.produto_produto_id = p.produto_id
            WHERE e.estoque_quantidade < 1
            """
            cursor.execute(sql)
            sem_estoque = cursor.fetchall()

            for item in sem_estoque:
                descricao = f"Sem estoque: {item['produto_nome']} ({item['estoque_quantidade']} unidades restantes)"
                Alertas.registrar_notificacao(cursor, descricao)
            conexao.commit()

            return sem_estoque #retorna os q estão abaixo de estoque
        finally: #fechamento de cursor e conexão
            cursor.close()
            conexao.close()

    @staticmethod
    def contar_vencidos():
        try:
            conexao = Database.connect() #abre conexão com o banco
            cursor = conexao.cursor(dictionary=True) #linhas voltam como dicionário

            #busca itens com validade anterior a hoje
            #converte o texto em data
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
            for item in vencidos: #para cada produto vencido é criado uma notificação
                descricao = (
                    f"Produto vencido: {item['produto_nome']} "
                    f"(validade {item['item_pedido_entrada_validade']})"
                )
                Alertas.registrar_notificacao(cursor, descricao)

            conexao.commit()
            return vencidos #retorna os vencidos
        finally: #fechamento de cursor e conexão
            cursor.close()
            conexao.close()
    
    @staticmethod
    def contar_data_relativa(): #def para contar dats relativas
        try:
            conexao = Database.connect() #abre conexão com o banco
            cursor = conexao.cursor(dictionary=True) #linhas voltam como dicionário

            #busca itens que vencem nos próximos 7 dias
            #também testa os formatos de data
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
            perto_vencimento = cursor.fetchall() #cria uma notificação "vence em breve" para cada item que está perto do vencimento
            for item in perto_vencimento:
                descricao = (
                    f"Vence em breve: {item['produto_nome']} "
                    f"(validade {item['item_pedido_entrada_validade']})"
                )
                Alertas.registrar_notificacao(cursor, descricao)

            conexao.commit()
            return perto_vencimento
        finally: #fechamento de cursor e conexão
            cursor.close() 
            conexao.close()
        
    @staticmethod
    def buscar_pendentes():
        conexao = Database.connect() #abre conexão com o banco
        cursor = conexao.cursor(dictionary=True) #linhas voltam como dicionário
        try: #lista as notificações pendentes, da mais recente para a mais antiga
            sql = """
            SELECT notificacao_id, notificacao_status, notificacao_data, notificacao_descricao
            FROM notificacao
            WHERE notificacao_status = 'pendente'
            ORDER BY notificacao_data DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally: #fechamento de cursor e conexão
            cursor.close()
            conexao.close()

        # Limites dos alertas dos sensores (ajuste conforme o ambiente)
    LIMITES_SENSORES = {
        "temperatura_min": 10,   # °C
        "temperatura_max": 21,   # °C
        "umidade_min": 50,   # %
        "luminosidade_max": 80,  # valor bruto do LDR
    }

    @staticmethod
    def verificar_sensores():
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            # última leitura de cada sensor
            sql = """
            SELECT
                s.sensor_n_serie, s.sensor_modelo,
                d.dados_sensor_temperatura,
                d.dados_sensor_umidade,
                d.dados_sensor_luminosidade
            FROM dados_sensor d
            INNER JOIN sensor s
                ON s.sensor_id = d.sensor_sensor_id
            WHERE d.dados_sensor_id IN (
                SELECT MAX(dados_sensor_id)
                FROM dados_sensor
                GROUP BY sensor_sensor_id
            )
            """
            cursor.execute(sql)
            leituras = cursor.fetchall()

            limite = Alertas.LIMITES_SENSORES
            alertas = []

            for l in leituras:
                n_serie = l["sensor_n_serie"]
                temperatura = l["dados_sensor_temperatura"]
                umidade = l["dados_sensor_umidade"]
                luminosidade = l["dados_sensor_luminosidade"]

                if temperatura is not None:
                    temperatura = float(temperatura)
                    if temperatura < limite["temperatura_min"]:
                        alertas.append(f"Temperatura baixa no sensor {n_serie} (abaixo de {limite['temperatura_min']}°C)")
                    elif temperatura > limite["temperatura_max"]:
                        alertas.append(f"Temperatura alta no sensor {n_serie} (acima de {limite['temperatura_max']}°C)")

                if umidade is not None:
                    umidade = float(umidade)
                    if umidade < limite["umidade_min"]:
                        alertas.append(f"Umidade baixa no sensor {n_serie} (abaixo de {limite['umidade_min']}%)")

                if luminosidade is not None and float(luminosidade) > limite["luminosidade_max"]:
                    alertas.append(f"Luminosidade alta no sensor {n_serie} (acima de {limite['luminosidade_max']}%)")
            for descricao in alertas:
                Alertas.registrar_notificacao(cursor,descricao)
            
            conexao.commit()
            return alertas 
        finally:
            cursor.close()
            conexao.close()