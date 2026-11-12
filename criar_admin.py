from models.usuario import Usuario
from core.securite import gerar_hash_senha

senha_hash = gerar_hash_senha("senha_do_admin")

caminho_imagem = "static/imagens/medicamento.jpg"

with open(caminho_imagem, "rb") as arquivo:
    imagem_blob = arquivo.read()

dados = {
    "usuario_nome": "Administrador",
    "usuario_email": "admin2@sistema.com",
    "usuario_senha": "123456",
    "usuario_cpf": "12345678901",
    "usuario_cargo": "adm",
    "usuario_imagem": "medicamento.jpg",  
    "imagem_tipo": "image/jpeg",           
    "imagem_blob": imagem_blob             
}

Usuario.inserir_usuario_adm(dados)

print("Usuário administrador criado com sucesso.")