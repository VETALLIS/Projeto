from models.usuario import Usuario

# Caminho da imagem padrão
caminho_imagem = "static/imagens/medicamento.jpg"

# Lê a imagem como binário (blob)
with open(caminho_imagem, "rb") as arquivo:
    imagem_blob = arquivo.read()

dados = {
    "usuario_nome": "Administrador",
    "usuario_email": "admin@sistema.com",
    "usuario_senha": "123456",
    "usuario_cpf": "12345678901",
    "usuario_cargo": "adm",
    "usuario_imagem": "medicamento.jpg",   # nome do arquivo
    "imagem_tipo": "image/jpeg",           # tipo mime
    "imagem_blob": imagem_blob             # conteúdo binário da imagem
}

Usuario.inserir_usuario_adm(dados)

print("Usuário administrador criado com sucesso.")