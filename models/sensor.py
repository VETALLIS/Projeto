from core.crud_base import Crud_base
from core.manipular import Manipular

class Sensor(Crud_base):
    tabela = "sensor"
    pk = "sensor_id"
    fields = ["sensor_nome", "sensor_descricao", "sensor_n_serie", "sensor_modelo", "sensor_voltagem", "sensor_tipo_conexao", "sensor_localizacao"]

    def __init__(self, sensor_nome, sensor_descricao, sensor_n_serie, sensor_modelo, sensor_voltagem, sensor_tipo_conexao, sensor_localizacao):
        self.sensor_nome = sensor_nome
        self.sensor_descricao = sensor_descricao
        self.sensor_n_serie = sensor_n_serie
        self.sensor_modelo = sensor_modelo
        self.sensor_voltagem = sensor_voltagem
        self.sensor_tipo_conexao = sensor_tipo_conexao
        self.sensor_localizacao = sensor_localizacao

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
        sensor = cls.buscar_tudo(order_by)

        if not sensor:
            raise ValueError("Sensor não encontrato")
        
        return sensor
