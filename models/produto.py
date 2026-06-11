from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database
import base64

class Produto(Crud_base):
    tabela = "produto"
    pk = "produto_id"
    fields = ["produto_nome", "produto_descricao", "produto_categoria", "usuario_usuario_id", "produto_imagem", "imagem_tipo", "imagem_blob"]

    def __init__(self, produto_nome, produto_descricao, produto_categoria, usuario_usuario_id=None, produto_imagem=None, imagem_tipo=None, imagem_blob=None, **kwargs):
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.usuario_usuario_id = usuario_usuario_id
        self.produto_imagem = produto_imagem
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob

    def validar_produto(self):
        erros = [
            Manipular.validar_vazio(self.produto_nome, "nome"),
            Manipular.validar_vazio(self.produto_categoria, "categoria")
        ]

        return [ erro for erro in erros if erro]
    
    def gravar_produto(self):
        produto = self.gravar()

        if not produto:
            raise ValueError("Erro ao cadastrar produto.")
        
        return "Cadastrado"
    
    @classmethod
    def relacao_entre_tabelas(cls, id):
        '''
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_movimentacao WHERE produto_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()'''
        return False

    @classmethod
    def deletar_produto(cls, id):
        produto = cls.buscar_por_id(id)

        if not produto:
            raise ValueError("Produto não encontrado.")
        if cls.relacao_entre_tabelas(id):
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.")
        cls.deletar(id)

        return "Produto deletado com sucesso!"
    
    def atualizar_produto(self, id):
        produto = self.buscar_por_id(id)

        if not produto:
            raise ValueError("Produto não encontrado!")
        if self.relacao_entre_tabelas(id):
            raise ValueError("Não é possível atualizar o produto porque ele possui pedidos ou movimentações vinculadas.")
        self.atualizar(id)

        return "Produto atualizado com sucesso!"
        
    @classmethod
    def buscar_produto_id(cls, id):
        produto = cls.buscar_por_id(id)

        if not produto:
            raise ValueError("Produto não encontrado")
        
        return produto

    @classmethod
    def buscar_todo_produto(cls, order_by="produto_nome"):
        produtos = cls.buscar_tudo(order_by)  

        if not produtos:
            raise ValueError("Produtos não encontrados")

        for produto in produtos:
            produto["imagem_base64"] = None
            if produto.get("imagem_blob"):
                produto["imagem_base64"] = base64.b64encode(produto["imagem_blob"]).decode("utf-8")

        return produtos

      @classmethod
    def filtro_categoria(cls, categoria):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"""select p.produto_categoria,  sum(e.estoque_quantidade) as estoque_quantidade from produto p
            join estoque e on e.produto_produto_id = p.produto_id
            where p.produto_categoria = %s
            group by p.produto_categoria;"""
            
            cursor.execute(sql, (f"%{categoria}%",))

            resultados = cursor.fetchall()

            if resultados:
                return resultados
            else:
                return None        
        finally:
            cursor.close()
            conexao.close()