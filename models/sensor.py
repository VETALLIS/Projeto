# importa a classe
from core.crud_base import Crud_base

# Cria a classe Sensor
class Sensor(Crud_base):
    # define a tabela, os campos e a PK, para o banco
    tabela = "sensor"
    pk = "sensor_id"
    fields = ["sensor_nome", "sensor_descricao", "sensor_n_serie", "sensor_modelo", "sensor_voltagem", "sensor_tipo_conexao", "sensor_localizacao"]

    # define os atributos
    def __init__(self, sensor_nome, sensor_descricao, sensor_n_serie, sensor_modelo, sensor_voltagem, sensor_tipo_conexao, sensor_localizacao):
        self.sensor_nome = sensor_nome
        self.sensor_descricao = sensor_descricao
        self.sensor_n_serie = sensor_n_serie
        self.sensor_modelo = sensor_modelo
        self.sensor_voltagem = sensor_voltagem
        self.sensor_tipo_conexao = sensor_tipo_conexao
        self.sensor_localizacao = sensor_localizacao

    # Métoso para gravar dados do sensor
    def gravar_sensor(self):
        sensor = self.gravar() # chama o método gravar 

        if not sensor: # verifica se foi gravado
            raise ValueError("Erro ao cadastrar sensor") # retorna o erro, se não foi cadastrado

        return "Sensor cadastrado com sucesso" # retorna sucesso

    # Método para deletar dados de um sensor
    @classmethod
    def deletar_sensor(cls, id):
        sensor = cls.buscar_por_id(id) # chama o método do Crud_base, para buscar o sensro

        if not sensor: # verifica se foi encontrado
            raise ValueError("Sensor não encontrado") # retorna se não foi encontrado
        
        cls.deletar(id) # chama a função deletar do Crud_base para deletar o sensor

        return "Sensor deletado com sucesso" # retorna sucesso 

    # Método para atualizar dados do sensor
    def atualizar_sensor(self, id):
        sensor = self.buscar_por_id(id) # chama o método co Crud_base, para buscar sensor

        if not sensor: # verifica se foi encontrado
            raise ValueError("Sensor não encontrado") # retorna erro, se não foi encontrado

        self.atualizar(id) # chama a função de atualizar do Crud_base
        return "Sensor atualizado com sucesso!" # retorna sucesso

    # Método para buscar sensor
    @classmethod
    def buscar_sensor(cls, id):
        sensor = cls.buscar_por_id(id) # chama o método do Crud_base para buscar sensor

        if not sensor: # verifica se foi encontrado
            raise ValueError("Sensor não encontrado") # retorna erro, se não foi encontrado

        sensor.pop("sensor_id", None) # tira o id do sensor para retornar para o usuario
        return Sensor(**sensor) # retorna os dados 