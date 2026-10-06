from core.crud_base import Crud_base #importação
from core.manipular import Manipular #importação
import base64 #importação

class Sensor(Crud_base):
    tabela = "sensor" #nome da tabela
    pk = "sensor_id" #chave primaria da tabela

    fields = ["sensor_nome", "sensor_descricao", "sensor_n_serie", "sensor_modelo", "sensor_voltagem", "sensor_tipo_conexao", "sensor_localizacao", "sensor_imagem", "imagem_blob",  "imagem_tipo"] #campos que temos na tela

    def __init__(self, sensor_nome, sensor_descricao, sensor_n_serie, sensor_modelo, sensor_voltagem, sensor_tipo_conexao, sensor_localizacao, sensor_imagem, imagem_tipo, imagem_blob): #definição de campos
        self.sensor_nome = sensor_nome
        self.sensor_descricao = sensor_descricao
        self.sensor_n_serie = sensor_n_serie
        self.sensor_modelo = sensor_modelo
        self.sensor_voltagem = sensor_voltagem
        self.sensor_tipo_conexao = sensor_tipo_conexao
        self.sensor_localizacao = sensor_localizacao
        self.sensor_imagem = sensor_imagem
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob

    def validar_sensor(self): #executa as validações e retorna o erro
        erros = [
            Manipular.validar_vazio(self.sensor_nome, "nome"), #campo não pode ser vazio
            Manipular.validar_vazio(self.sensor_descricao, "descrição"), #campo não pode ser vazio
            Manipular.validar_vazio(self.sensor_n_serie, "Numero de serie"), #campo não pode ser vazio
            Manipular.validar_vazio(self.sensor_modelo, "Modelo"), #campo não pode ser vazio
            Manipular.validar_vazio(self.sensor_voltagem, "voltagem"), #campo não pode ser vazio
            Manipular.validar_vazio(self.sensor_tipo_conexao, "Tipo conexão"), #campo não pode ser vazio
            Manipular.validar_vazio(self.sensor_localizacao, "Localização"), #campo não pode ser vazio
            Manipular.validar_numero(self.sensor_n_serie, "Numero de serie") #o campo nuemro de serie precisa tem numero
        ]  #chamando as validações que serão usadas nessa tela, elas veem do manipular.py   
            
        return [ erro for erro in erros if erro] #retorna o erro

    def gravar_sensor(self): #def para gravar sensor no banco
        sensor = self.gravar() 

        if not sensor:
            raise ValueError("Erro ao cadastrar sensor")

        return "Sensor cadastrado com sucesso" #mensagem de retorno

    @classmethod 
    def deletar_sensor(cls, id): #deletar sensor 
        sensor = cls.buscar_por_id(id) #busca sesnor por id

        if not sensor:
            raise ValueError("Sensor não encontrado") #se o sensor não for encontrado, ele retorna a mensagem
        cls.deletar(id) #deleta sensor se encontrar
        return "Sensor deletado com sucesso" #se encontrar deleta e retorna essa mensagem











    def atualizar_sensor(self, id): #def para salvar atualização do sensor
        sensor = self.buscar_por_id(id)

        if not sensor:
            raise ValueError("Sensor não encontrado")

        self.atualizar(id)
        return "Sensor atualizado com sucesso!"

    @classmethod #buscando po id
    def buscar_sensor_id(cls, id):
        sensor = cls.buscar_por_id(id)

        if not sensor:
            raise ValueError("Sensor não encontrado")
            
        sid = sensor["sensor_id"]      
        del sensor["sensor_id"]        
        obj = Sensor(**sensor)         
        obj.sensor_id = sid
        if obj.imagem_blob:
            obj.imagem_base64 = base64.b64encode(obj.imagem_blob).decode("utf-8")
        else:
            obj.imagem_base64 = ""
        return obj
    
    @classmethod #buscando imagem para sensor
    def buscar_sensores(cls, order_by=pk):
        sensores = cls.buscar_tudo(order_by)

        if not sensores:
            raise ValueError("Sensor não encontrato")
        
        for sensor in sensores:
            sensor["imagem_base64"] = None
            if sensor.get("imagem_blob"):
                sensor["imagem_base64"] = base64.b64encode(sensor["imagem_blob"]).decode("utf-8")
            else:
                sensor["imagem_base64"] = None
        return sensores
    
    @classmethod #analisa os dados cadastrados, com o banco
    def contar_sensores(cls, order_by="sensor_id"):
        sensor = cls.buscar_tudo(order_by)
        if not sensor:
            raise ValueError("Sensor não encontrato")
        
        sensores = 0
        for i in sensor:
            sensores = sensores + 1
        return sensores
