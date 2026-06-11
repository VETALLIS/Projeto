from core.crud_base import Crud_base
from core.manipular import Manipular
import base64

class Sensor(Crud_base):
    tabela = "sensor"
    pk = "sensor_id"
    fields = ["sensor_nome", "sensor_descricao", "sensor_n_serie", "sensor_modelo", "sensor_voltagem", "sensor_tipo_conexao", "sensor_localizacao", "sensor_imagem", "imagem_blob",  "imagem_tipo"]

    def __init__(self, sensor_nome, sensor_descricao, sensor_n_serie, sensor_modelo, sensor_voltagem, sensor_tipo_conexao, sensor_localizacao, sensor_imagem, imagem_tipo, imagem_blob):
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

    def validar_sensor(self):
        erros = [
            Manipular.validar_vazio(self.sensor_nome, "nome"),
            Manipular.validar_vazio(self.sensor_descricao, "descrição"),
            Manipular.validar_vazio(self.sensor_n_serie, "Numero de serie"),
            Manipular.validar_vazio(self.sensor_modelo, "Modelo"),
            Manipular.validar_vazio(self.sensor_voltagem, "voltagem"),
            Manipular.validar_vazio(self.sensor_tipo_conexao, "Tipo conexão"),
            Manipular.validar_vazio(self.sensor_localizacao, "Localização")
        ]     
            
        return [ erro for erro in erros if erro]

    def gravar_sensor(self):
        sensor = self.gravar()

        if not sensor:
            raise ValueError("Erro ao cadastrar sensor")

        return "Sensor cadastrado com sucesso"

    @classmethod
    def deletar_sensor(cls, id):
        sensor = cls.buscar_por_id(id)

        if not sensor:
            raise ValueError("Sensor não encontrado")
        cls.deletar(id)
        return "Sensor deletado com sucesso" 

    def atualizar_sensor(self, id):
        sensor = self.buscar_por_id(id)

        if not sensor:
            raise ValueError("Sensor não encontrado")

        self.atualizar(id)
        return "Sensor atualizado com sucesso!"

    @classmethod
    def buscar_sensor_id(cls, id):
        sensor = cls.buscar_por_id(id)

        if not sensor:
            raise ValueError("Sensor não encontrado")
            
        sid = sensor["sensor_id"]      
        del sensor["sensor_id"]        
        obj = Sensor(**sensor)         
        obj.sensor_id = sid
        return obj
    
    @classmethod
    def buscar_sensores(cls, order_by=pk):
        sensores = cls.buscar_tudo(order_by)

        if not sensores:
            raise ValueError("Sensor não encontrato")
        
        for sensor in sensores:
            sensor["imagem_base64"] = None
            if sensor.get("imagem_blob"):
                sensor["imagem_base64"] = base64.b64encode(sensor["imagem_blob"]).decode("utf-8")
        
        return sensores
    
    @classmethod
    def contar_sensores(cls, order_by="sensor_id"):
        sensor = cls.buscar_tudo(order_by)
        if not sensor:
            raise ValueError("Sensor não encontrato")
        
        sensores = 0
        for i in sensor:
            sensores = sensores + 1
        return sensores
