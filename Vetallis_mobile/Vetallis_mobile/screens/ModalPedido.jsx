import React, { useState } from 'react';
import {
  Modal,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function ModalPedido({
  visible,
  tipo, // 'entrada' ou 'saida'
  produtosDisponiveis, // [{ id, nome, estoque_quantidade }]
  onClose,
  onConfirmar, // (pedidoCompleto) => Promise/void
}) {
  const labelReferencia = tipo === 'entrada' ? 'Fornecedor' : 'Animal';

  // ---- CABEÇALHO DO PEDIDO ----
  const [nome, setNome] = useState('');
  const [dataPedido, setDataPedido] = useState('');
  const [referencia, setReferencia] = useState('');

  // ---- ITEM ATUAL SENDO PREENCHIDO ----
  const [produtoSelecionado, setProdutoSelecionado] = useState(null);
  const [lote, setLote] = useState('');
  const [qtd, setQtd] = useState('');
  const [valorUnitario, setValorUnitario] = useState('');
  const [dataItem, setDataItem] = useState('');

  // ---- LISTA DE ITENS JÁ ADICIONADOS ----
  const [itens, setItens] = useState([]);

  // ---- SELETOR DE PRODUTO ----
  const [seletorVisible, setSeletorVisible] = useState(false);

  // ---- ESTADO DE ENVIO ----
  const [enviando, setEnviando] = useState(false);
  const [erroValidacao, setErroValidacao] = useState('');

  function limparCampos() {
    setNome('');
    setDataPedido('');
    setReferencia('');
    setItens([]);
    setErroValidacao('');
    limparItemAtual();
  }

  function limparItemAtual() {
    setProdutoSelecionado(null);
    setLote('');
    setQtd('');
    setValorUnitario('');
    setDataItem('');
  }

  function adicionarItem() {
    if (!produtoSelecionado) {
      setErroValidacao('Selecione um produto');
      return;
    }
    if (!qtd || isNaN(qtd) || Number(qtd) <= 0) {
      setErroValidacao('Informe uma quantidade válida');
      return;
    }
    setErroValidacao('');
    setItens((prev) => [
      ...prev,
      {
        produto_id: produtoSelecionado.id,
        produto_nome: produtoSelecionado.nome,
        lote,
        qtd: Number(qtd),
        valor_unitario: valorUnitario ? Number(valorUnitario) : null,
        data: dataItem,
      },
    ]);
    limparItemAtual();
  }

  function removerItem(index) {
    setItens((prev) => prev.filter((_, i) => i !== index));
  }

  async function handleConfirmar() {
    if (!nome || !dataPedido || !referencia) {
      setErroValidacao(`Preencha nome, data e ${labelReferencia.toLowerCase()}`);
      return;
    }
    if (itens.length === 0) {
      setErroValidacao('Adicione ao menos um item ao pedido');
      return;
    }

    const pedido = {
      tipo,
      nome,
      data: dataPedido,
      [tipo === 'entrada' ? 'fornecedor' : 'animal']: referencia,
      itens,
    };

    setEnviando(true);
    setErroValidacao('');
    try {
      await onConfirmar(pedido);
      limparCampos();
      onClose();
    } catch (err) {
      setErroValidacao(err.message || 'Erro ao enviar pedido');
    } finally {
      setEnviando(false);
    }
  }

  function handleCancelar() {
    limparCampos();
    onClose();
  }

  return (
    <Modal visible={visible} animationType="slide" onRequestClose={handleCancelar}>
      <View style={styles.tela}>
        <ScrollView contentContainerStyle={{ paddingBottom: 40 }} showsVerticalScrollIndicator={false}>
          <Text style={styles.titulo}>
            {tipo === 'entrada' ? 'Entrada de produtos' : 'Saída de produtos'}
          </Text>

          {/* ---- BLOCO PEDIDO ---- */}
          <Text style={styles.secao}>Pedido</Text>
          <View style={styles.linha}>
            <View style={{ flex: 2, marginRight: 10 }}>
              <Text style={styles.label}>Nome:</Text>
              <TextInput style={styles.input} value={nome} onChangeText={setNome} placeholder="Nome" />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.label}>Data:</Text>
              <TextInput
                style={styles.input}
                value={dataPedido}
                onChangeText={setDataPedido}
                placeholder="DD/MM/AAAA"
              />
            </View>
          </View>

          <Text style={styles.label}>{labelReferencia}:</Text>
          <TextInput
            style={styles.input}
            value={referencia}
            onChangeText={setReferencia}
            placeholder={`Selecione o ${labelReferencia.toLowerCase()}`}
          />

          {/* ---- BLOCO ITEM DO PEDIDO ---- */}
          <Text style={styles.secao}>Item do pedido</Text>

          <Text style={styles.label}>Produto:</Text>
          <TouchableOpacity style={styles.seletorProduto} onPress={() => setSeletorVisible(true)}>
            <Text style={{ color: produtoSelecionado ? '#000' : '#888' }}>
              {produtoSelecionado ? produtoSelecionado.nome : 'Selecione'}
            </Text>
            <Ionicons name="chevron-down" size={18} color="#555" />
          </TouchableOpacity>

          <View style={styles.linha}>
            <View style={{ flex: 1, marginRight: 10 }}>
              <Text style={styles.label}>Qtd:</Text>
              <TextInput
                style={styles.input}
                keyboardType="numeric"
                value={qtd}
                onChangeText={setQtd}
                placeholder="0"
              />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.label}>Lote:</Text>
              <TextInput style={styles.input} value={lote} onChangeText={setLote} placeholder="Lote" />
            </View>
          </View>

          <View style={styles.linha}>
            <View style={{ flex: 1, marginRight: 10 }}>
              <Text style={styles.label}>Valor uni.:</Text>
              <TextInput
                style={styles.input}
                keyboardType="numeric"
                value={valorUnitario}
                onChangeText={setValorUnitario}
                placeholder="0,00"
              />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.label}>Data:</Text>
              <TextInput
                style={styles.input}
                value={dataItem}
                onChangeText={setDataItem}
                placeholder="DD/MM/AAAA"
              />
            </View>
          </View>

          <TouchableOpacity style={styles.botaoAdicionarItem} onPress={adicionarItem}>
            <Ionicons name="add" size={18} color="#03A64A" />
            <Text style={styles.textoAdicionarItem}>Adicionar item</Text>
          </TouchableOpacity>

          {/* ---- LISTA DE ITENS ADICIONADOS ---- */}
          {itens.length > 0 && (
            <View style={{ marginTop: 16 }}>
              <Text style={styles.secao}>Itens adicionados ({itens.length})</Text>
              {itens.map((item, index) => (
                <View key={index} style={styles.itemRow}>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.itemNome}>{item.produto_nome}</Text>
                    <Text style={styles.itemDetalhe}>
                      Qtd: {item.qtd} {item.lote ? `• Lote: ${item.lote}` : ''}
                    </Text>
                  </View>
                  <TouchableOpacity onPress={() => removerItem(index)}>
                    <Ionicons name="trash-outline" size={20} color="#bd0404" />
                  </TouchableOpacity>
                </View>
              ))}
            </View>
          )}

          {erroValidacao !== '' && (
            <Text style={styles.mensagemErro}>{erroValidacao}</Text>
          )}

          {/* ---- BOTÕES FINAIS ---- */}
          <View style={styles.botoesFinais}>
            <TouchableOpacity style={styles.botaoCancelar} onPress={handleCancelar} disabled={enviando}>
              <Text style={styles.textoBotao}>Cancelar</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.botaoConfirmar,
                { backgroundColor: tipo === 'entrada' ? '#03A64A' : '#bd0404' },
                enviando && { opacity: 0.6 },
              ]}
              onPress={handleConfirmar}
              disabled={enviando}
            >
              <Text style={styles.textoBotao}>{enviando ? 'Enviando...' : 'Confirmar'}</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>

      {/* ---- MODAL SECUNDÁRIO: SELETOR DE PRODUTO ---- */}
      <Modal visible={seletorVisible} animationType="fade" transparent onRequestClose={() => setSeletorVisible(false)}>
        <View style={styles.overlaySeletor}>
          <View style={styles.caixaSeletor}>
            <Text style={styles.tituloSeletor}>Selecione o produto</Text>
            <FlatList
              data={produtosDisponiveis}
              keyExtractor={(item) => String(item.id)}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={styles.produtoOpcao}
                  onPress={() => {
                    setProdutoSelecionado(item);
                    setSeletorVisible(false);
                  }}
                >
                  <Text style={styles.produtoOpcaoNome}>{item.nome}</Text>
                  <Text style={styles.produtoOpcaoEstoque}>Estoque: {item.estoque_quantidade}</Text>
                </TouchableOpacity>
              )}
              ItemSeparatorComponent={() => <View style={styles.separador} />}
              ListEmptyComponent={
                <Text style={{ textAlign: 'center', color: '#999', padding: 20 }}>
                  Nenhum produto disponível
                </Text>
              }
            />
            <TouchableOpacity onPress={() => setSeletorVisible(false)} style={{ marginTop: 12 }}>
              <Text style={{ color: '#bd0404', textAlign: 'center' }}>Fechar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </Modal>
  );
}

const styles = StyleSheet.create({
  tela: { flex: 1, backgroundColor: '#0a4a3a', padding: 20, paddingTop: 60 },
  titulo: { color: '#fff', fontSize: 26, fontWeight: 'bold', marginBottom: 20 },
  secao: { color: '#fff', fontSize: 18, fontWeight: 'bold', marginTop: 16, marginBottom: 10 },
  linha: { flexDirection: 'row', marginBottom: 4 },
  label: { color: '#e0e0e0', marginBottom: 6, marginTop: 10 },
  input: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 12,
  },
  seletorProduto: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  botaoAdicionarItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ffffff22',
    borderRadius: 10,
    padding: 12,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#03A64A',
  },
  textoAdicionarItem: { color: '#03A64A', fontWeight: 'bold', marginLeft: 6 },
  itemRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff15',
    borderRadius: 10,
    padding: 12,
    marginBottom: 8,
  },
  itemNome: { color: '#fff', fontWeight: 'bold' },
  itemDetalhe: { color: '#ccc', fontSize: 12, marginTop: 2 },
  mensagemErro: {
    color: '#ffb3b3',
    marginTop: 16,
    textAlign: 'center',
    fontWeight: '600',
  },
  botoesFinais: { flexDirection: 'row', marginTop: 30, gap: 12 },
  botaoCancelar: {
    flex: 1,
    backgroundColor: '#555',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  botaoConfirmar: {
    flex: 1,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  textoBotao: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  overlaySeletor: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'center',
    padding: 30,
  },
  caixaSeletor: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    maxHeight: '70%',
  },
  tituloSeletor: { fontWeight: 'bold', fontSize: 16, marginBottom: 12 },
  produtoOpcao: { paddingVertical: 10 },
  produtoOpcaoNome: { fontSize: 15, fontWeight: '500' },
  produtoOpcaoEstoque: { fontSize: 12, color: '#777', marginTop: 2 },
  separador: { height: 1, backgroundColor: '#eee' },
});