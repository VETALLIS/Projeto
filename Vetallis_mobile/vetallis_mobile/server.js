const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Configuração da Conexão com o MySQL
const db = mysql.createPool({
  host: 'localhost',
  user: 'root',        // Altere para seu usuário do MySQL
  password: '123456',  // Altere para sua senha do MySQL
  database: 'vetallis_db_2_2',
  waitForConnections: true,
  connectionLimit: 10,
});

/* ---------------------------------------------------------------------
   OBSERVAÇÕES SOBRE O SCHEMA (vetallis_db_2_2)
   - Usuários -> tabela `usuario` (usuario_id, usuario_email, usuario_senha, usuario_nome, usuario_cargo...)
   - Produtos -> tabela `produto` (PK composta: produto_id + usuario_usuario_id)
   - Estoque  -> tabela `estoque` (estoque_quantidade é VARCHAR, por isso usamos CAST(... AS UNSIGNED))
   - Movimentações "de verdade" ficam em pedido_entrada/item_pedido_entrada
     (exige fornecedor_fornecedor_id) e pedido_saida/item_pedido_saida
     (exige animal_animal_id). Como a rota abaixo só recebe produtoId/tipo/quantidade,
     a movimentação apenas ajusta o saldo em `estoque`; se quiser registrar o pedido
     completo (com fornecedor ou animal), me avise que eu adapto a rota.
--------------------------------------------------------------------- */

// 1. Rota de Login
app.post('/api/login', async (req, res) => {
  const { email, senha } = req.body;
  try {
    const [linhas] = await db.query(
      `SELECT usuario_id AS id, usuario_nome AS nome, usuario_email AS email, usuario_cargo AS cargo
       FROM usuario
       WHERE usuario_email = ? AND usuario_senha = ?`,
      [email, senha]
    );
    if (linhas.length > 0) {
      res.json({ sucesso: true, usuario: linhas[0] });
    } else {
      res.status(401).json({ sucesso: false, mensagem: 'Credenciais inválidas.' });
    }
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 2. Rota de Painel (Resumo)
app.get('/api/painel', async (req, res) => {
  try {
    const [[{ totalProdutos }]] = await db.query(
      `SELECT SUM(CAST(estoque_quantidade AS UNSIGNED)) AS totalProdutos FROM estoque`
    );
    const [[{ estoqueBaixoCount }]] = await db.query(
      `SELECT COUNT(*) AS estoqueBaixoCount FROM estoque WHERE CAST(estoque_quantidade AS UNSIGNED) <= 5`
    );
    const [atividadesRecentes] = await db.query(`
      (SELECT ipe.item_pedido_entrada_id AS id, 'Entrada' AS tipo,
              ipe.item_pedido_entrada_quantidade AS quantidade,
              pr.produto_nome AS produto, pe.pedido_entrada_data AS data
       FROM item_pedido_entrada ipe
       JOIN estoque e ON ipe.estoque_estoque_id = e.estoque_id
       JOIN produto pr ON e.produto_produto_id = pr.produto_id
       JOIN pedido_entrada pe ON ipe.pedido_entrada_pedido_entrada_id = pe.pedido_entrada_id)
      UNION ALL
      (SELECT ips.item_pedido_saida_id AS id, 'Saída' AS tipo,
              ips.item_pedido_saida_quantidade AS quantidade,
              pr.produto_nome AS produto, ps.pedido_saida_data AS data
       FROM item_pedido_saida ips
       JOIN estoque e ON ips.estoque_estoque_id = e.estoque_id
       JOIN produto pr ON e.produto_produto_id = pr.produto_id
       JOIN pedido_saida ps ON ips.pedido_saida_pedido_saida_id = ps.pedido_saida_id)
      ORDER BY id DESC
      LIMIT 5
    `);

    res.json({
      totalProdutos: totalProdutos || 0,
      estoqueBaixoCount: estoqueBaixoCount || 0,
      atividadesRecentes,
    });
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 3. Listar Produtos (com quantidade em estoque)
app.get('/api/produtos', async (req, res) => {
  try {
    const [produtos] = await db.query(`
      SELECT p.produto_id AS id,
             p.produto_nome AS nome,
             p.produto_descricao AS descricao,
             p.produto_categoria AS categoria,
             (p.imagem_blob IS NOT NULL) AS temImagem,
             COALESCE(CAST(e.estoque_quantidade AS UNSIGNED), 0) AS quantidade
      FROM produto p
      LEFT JOIN estoque e ON e.produto_produto_id = p.produto_id
                          AND e.produto_usuario_usuario_id = p.usuario_usuario_id
      ORDER BY p.produto_nome ASC
    `);
    res.json(produtos);
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 4. Buscar Produto Específico por ID
app.get('/api/produtos/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const [linhas] = await db.query(
      `SELECT p.produto_id AS id,
              p.produto_nome AS nome,
              p.produto_descricao AS descricao,
              p.produto_categoria AS categoria,
              (p.imagem_blob IS NOT NULL) AS temImagem,
              COALESCE(CAST(e.estoque_quantidade AS UNSIGNED), 0) AS quantidade
       FROM produto p
       LEFT JOIN estoque e ON e.produto_produto_id = p.produto_id
                           AND e.produto_usuario_usuario_id = p.usuario_usuario_id
       WHERE p.produto_id = ?`,
      [id]
    );
    if (linhas.length > 0) {
      res.json(linhas[0]);
    } else {
      res.status(404).json({ mensagem: 'Produto não encontrado' });
    }
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 4b. Servir a Imagem do Produto (armazenada como BLOB)
app.get('/api/produtos/:id/imagem', async (req, res) => {
  const { id } = req.params;
  try {
    const [linhas] = await db.query(
      `SELECT imagem_blob, imagem_tipo FROM produto WHERE produto_id = ? LIMIT 1`,
      [id]
    );
    if (linhas.length === 0 || !linhas[0].imagem_blob) {
      return res.status(404).json({ mensagem: 'Imagem não encontrada' });
    }
    res.set('Content-Type', linhas[0].imagem_tipo || 'image/jpeg');
    res.send(linhas[0].imagem_blob);
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 5. Movimentação de Estoque (Entrada / Saída)
// Ajusta diretamente o saldo em `estoque`. Não cria pedido_entrada/pedido_saida
// completos (isso exigiria fornecedor_id ou animal_id).
app.post('/api/estoque/movimentar', async (req, res) => {
  const { produtoId, tipo, quantidade } = req.body;
  const qtdNum = parseInt(quantidade, 10);

  if (!produtoId || !tipo || isNaN(qtdNum) || qtdNum <= 0) {
    return res.status(400).json({ mensagem: 'Dados inválidos.' });
  }

  const connection = await db.getConnection();
  try {
    await connection.beginTransaction();

    const sqlEstoque = tipo === 'Entrada'
      ? `UPDATE estoque
         SET estoque_quantidade = CAST(CAST(estoque_quantidade AS UNSIGNED) + ? AS CHAR)
         WHERE produto_produto_id = ?`
      : `UPDATE estoque
         SET estoque_quantidade = CAST(CAST(estoque_quantidade AS UNSIGNED) - ? AS CHAR)
         WHERE produto_produto_id = ? AND CAST(estoque_quantidade AS UNSIGNED) >= ?`;

    const parametros = tipo === 'Entrada'
      ? [qtdNum, produtoId]
      : [qtdNum, produtoId, qtdNum];

    const [resultado] = await connection.query(sqlEstoque, parametros);

    if (resultado.affectedRows === 0) {
      await connection.rollback();
      return res.status(400).json({ mensagem: 'Estoque insuficiente ou produto não encontrado.' });
    }

    await connection.commit();
    res.json({ sucesso: true, mensagem: 'Movimentação realizada com sucesso!' });
  } catch (erro) {
    await connection.rollback();
    res.status(500).json({ erro: erro.message });
  } finally {
    connection.release();
  }
});

// 6. Listar Histórico Completo (entradas + saídas)
app.get('/api/historico', async (req, res) => {
  try {
    const [linhas] = await db.query(`
      (SELECT ipe.item_pedido_entrada_id AS id, 'Entrada' AS tipo,
              ipe.item_pedido_entrada_quantidade AS quantidade,
              pe.pedido_entrada_data AS data, NULL AS hora,
              pr.produto_nome AS produto
       FROM item_pedido_entrada ipe
       JOIN estoque e ON ipe.estoque_estoque_id = e.estoque_id
       JOIN produto pr ON e.produto_produto_id = pr.produto_id
       JOIN pedido_entrada pe ON ipe.pedido_entrada_pedido_entrada_id = pe.pedido_entrada_id)
      UNION ALL
      (SELECT ips.item_pedido_saida_id AS id, 'Saída' AS tipo,
              ips.item_pedido_saida_quantidade AS quantidade,
              ps.pedido_saida_data AS data, NULL AS hora,
              pr.produto_nome AS produto
       FROM item_pedido_saida ips
       JOIN estoque e ON ips.estoque_estoque_id = e.estoque_id
       JOIN produto pr ON e.produto_produto_id = pr.produto_id
       JOIN pedido_saida ps ON ips.pedido_saida_pedido_saida_id = ps.pedido_saida_id)
      ORDER BY id DESC
    `);
    res.json(linhas);
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 7. Buscar Usuário Específico por ID
app.get('/api/usuarios/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const [linhas] = await db.query(
      `SELECT usuario_id AS id, usuario_nome AS nome, usuario_email AS email, usuario_cargo AS cargo
       FROM usuario WHERE usuario_id = ?`,
      [id]
    );
    if (linhas.length > 0) {
      res.json(linhas[0]);
    } else {
      res.status(404).json({ mensagem: 'Usuário não encontrado' });
    }
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 8. Atualizar Usuário (nome, email e/ou cargo)
app.put('/api/usuarios/:id', async (req, res) => {
  const { id } = req.params;
  const { nome, email, cargo } = req.body;

  if (!nome && !email && !cargo) {
    return res.status(400).json({ mensagem: 'Nenhum dado para atualizar.' });
  }

  try {
    const campos = [];
    const valores = [];
    if (nome) { campos.push('usuario_nome = ?'); valores.push(nome); }
    if (email) { campos.push('usuario_email = ?'); valores.push(email); }
    if (cargo) { campos.push('usuario_cargo = ?'); valores.push(cargo); }
    valores.push(id);

    const [resultado] = await db.query(
      `UPDATE usuario SET ${campos.join(', ')} WHERE usuario_id = ?`,
      valores
    );

    if (resultado.affectedRows === 0) {
      return res.status(404).json({ mensagem: 'Usuário não encontrado' });
    }

    const [linhas] = await db.query(
      `SELECT usuario_id AS id, usuario_nome AS nome, usuario_email AS email, usuario_cargo AS cargo
       FROM usuario WHERE usuario_id = ?`,
      [id]
    );

    res.json({ sucesso: true, usuario: linhas[0] });
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

// 9. Excluir Usuário
app.delete('/api/usuarios/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const [resultado] = await db.query('DELETE FROM usuario WHERE usuario_id = ?', [id]);
    if (resultado.affectedRows === 0) {
      return res.status(404).json({ mensagem: 'Usuário não encontrado' });
    }
    res.json({ sucesso: true, mensagem: 'Usuário excluído com sucesso.' });
  } catch (erro) {
    res.status(500).json({ erro: erro.message });
  }
});

const PORTA = 3000;
app.listen(PORTA, () => console.log(`Servidor rodando em http://localhost:${PORTA}`));