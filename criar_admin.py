from models.usuario import Usuario



dados = {
    "usuario_nome": "Administrador",
    "usuario_email": "admin@sistema.com",
    "usuario_senha": "123456",
    "usuario_cpf": "12345678901",
    "usuario_cargo": "admin"
}

Usuario.inserir_usuario_adm(dados)

print("Usuário administrador criado com sucesso.")