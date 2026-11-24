import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Image, RefreshControl } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useState, useEffect } from 'react';
import ModalPedido from './ModalPedido';
import { API_URL } from '../src/services/api';

// Deixe true enquanto estiver investigando. Mostra na tela o endereço da API e o resultado de cada chamada.
// Quando tudo funcionar, troque para false.
const MOSTRAR_DIAGNOSTICO = true;

// Busca uma lista na API. Nunca lança erro: devolve { lista, erro }.
async function buscarLista(caminho) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(`${API_URL}${caminho}`, { signal: controller.signal });
    const texto = await res.text();

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    let data;
    try {
      data = JSON.parse(texto);
    } catch {
      throw new Error(`Resposta não é JSON: ${texto.slice(0, 60)}`);
    }

    if (!Array.isArray(data)) {
      throw new Error(`Formato inesperado: ${JSON.stringify(data).slice(0, 80)}`);
    }

    return { lista: data, erro: null };
  } catch (err) {
    const erro =
      err.name === 'AbortError'
        ? 'Tempo esgotado: o servidor não respondeu'
        : err.message || 'Falha de conexão';
    return { lista: [], erro };
  } finally {
    clearTimeout(timer);
  }
}

export default function LeitorScreen() {
  const [mensagem, setMensagem] = useState('');
  const [sucesso, setSucesso] = useState('');
  const [atualizando, setAtualizando] = useState(false);

  // ---- ESTADOS DO MODAL DE PEDIDO ----
  const [modalVisible, setModalVisible] = useState(false);
  const [tipoMovimentacao, setTipoMovimentacao] = useState(null); // 'entrada' | 'saida'
  const [produtosEstoque, setProdutosEstoque] = useState([]);
  const [fornecedores, setFornecedores] = useState([]);
  const [animais, setAnimais] = useState([]);
  const [carregandoProdutos, setCarregandoProdutos] = useState(false);

  // ---- DIAGNÓSTICO: resultado de cada chamada ----
  const [erros, setErros] = useState({ produtos: null, fornecedores: null, animais: null });

  useEffect(() => {
    carregarProdutos();
    carregarFornecedores();
    carregarAnimais();
  }, []);

  async function carregarProdutos() {
    setCarregandoProdutos(true);
    const { lista, erro } = await buscarLista('/api/produtos');
    setProdutosEstoque(lista);
    setErros((e) => ({ ...e, produtos: erro }));
    if (erro) console.log('Erro em /api/produtos:', erro);
    setCarregandoProdutos(false);
  }

  async function carregarFornecedores() {
    const { lista, erro } = await buscarLista('/api/fornecedores');
    setFornecedores(lista);
    setErros((e) => ({ ...e, fornecedores: erro }));
    if (erro) console.log('Erro em /api/fornecedores:', erro);
  }

  async function carregarAnimais() {
    const { lista, erro } = await buscarLista('/api/animais');
    setAnimais(lista);
    setErros((e) => ({ ...e, animais: erro }));
    if (erro) console.log('Erro em /api/animais:', erro);
  }

  // Puxar a tela pra baixo recarrega tudo
  async function atualizarTudo() {
    setAtualizando(true);
    await Promise.all([carregarProdutos(), carregarFornecedores(), carregarAnimais()]);
    setAtualizando(false);
  }

  // Listas já formatadas pro formato que o ModalPedido espera ({ id, nome, subtitulo })
  const fornecedoresFormatados = fornecedores.map((f, i) => ({
    id: f.fornecedor_id ?? i,
    nome: f.fornecedor_nome ?? f.nome ?? '(sem nome)',
    subtitulo: f.fornecedor_tipo_produtos ?? f.tipo_produtos ?? '',
  }));

  const animaisFormatados = animais.map((a, i) => ({
    id: a.animal_id ?? a.id ?? i,
    nome: a.animal_identificacao ?? a.nome ?? '(sem nome)',
    subtitulo: [a.animal_especie, a.animal_raca].filter(Boolean).join(' • '),
  }));

  // Produtos no formato que o ModalPedido espera ({ id, nome, estoque_quantidade })
  // A API devolve { id, nome, quantidade, ... }
  const produtosFormatados = produtosEstoque.map((p, i) => ({
    id: p.id ?? p.produto_id ?? i,
    nome: p.nome ?? p.produto_nome,
    estoque_quantidade: p.quantidade ?? p.estoque_quantidade ?? 0,
  }));

  // Escolhe a lista certa de acordo com o tipo de movimentação aberto
  const referenciasDoModal = tipoMovimentacao === 'entrada' ? fornecedoresFormatados : animaisFormatados;

  function abrirModalPedido(tipo) {
    setTipoMovimentacao(tipo);
    setModalVisible(true);
  }

  async function enviarPedido(pedido) {
    try {
      const response = await fetch(`${API_URL}/api/pedidos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pedido),
      });

      const resultado = await response.json();

      if (!response.ok) {
        throw new Error(resultado.erro || 'Erro ao registrar pedido');
      }

      setMensagem(
        pedido.tipo === 'entrada'
          ? 'Entrada registrada com sucesso'
          : 'Saída registrada com sucesso'
      );
      setSucesso(true);
      carregarProdutos();
    } catch (err) {
      setMensagem(err.message);
      setSucesso(false);
      throw err;
    }
  }

  const temErro = erros.produtos || erros.fornecedores || erros.animais;

  return (
    <LinearGradient
      colors={['#000000', '#0d3b2e', '#0a4a3a', '#1a6b4a']}
      locations={[0, 0.3, 0.6, 1]}
      start={{ x: 0.2, y: 0.1 }}
      end={{ x: 1, y: 1 }}
      style={styles.container}
    >
      <View style={styles.menu}>
        <View style={styles.menuEsquerda}>
          <Image
            source={require('../assets/vetallis.png')}
            style={styles.logo}
          />
        </View>
      </View>

      <View style={styles.header}>
        <Text style={styles.title}>Movimentação de produtos</Text>
      </View>

      <ScrollView
        contentContainerStyle={{ paddingBottom: 30 }}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={atualizando} onRefresh={atualizarTudo} tintColor="#fff" colors={['#03A64A']} />
        }
      >
        {/* ---- DIAGNÓSTICO (remova quando tudo funcionar: MOSTRAR_DIAGNOSTICO = false) ---- */}
        {MOSTRAR_DIAGNOSTICO && (
          <View style={styles.diagnostico}>
            <Text style={styles.diagnosticoTitulo}>Diagnóstico</Text>
            <Text style={styles.diagnosticoLinha}>API_URL: {String(API_URL)}</Text>
            <Text style={styles.diagnosticoLinha}>
              Produtos: {erros.produtos ? `ERRO - ${erros.produtos}` : `${produtosEstoque.length} itens`}
            </Text>
            <Text style={styles.diagnosticoLinha}>
              Fornecedores: {erros.fornecedores ? `ERRO - ${erros.fornecedores}` : `${fornecedores.length} itens`}
            </Text>
            <Text style={styles.diagnosticoLinha}>
              Animais: {erros.animais ? `ERRO - ${erros.animais}` : `${animais.length} itens`}
            </Text>
            {temErro && (
              <Text style={styles.diagnosticoDica}>
                Puxe a tela para baixo para tentar de novo.
              </Text>
            )}
          </View>
        )}

        {/* ---- BOTÕES ---- */}
        <View style={styles.botoesLinha}>
          <TouchableOpacity style={styles.botao} onPress={() => abrirModalPedido('entrada')}>
            <MaterialCommunityIcons name="plus-circle-outline" size={22} color="#fff" />
            <Text style={styles.textoBotao}>Adicionar produto</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.botao_saida} onPress={() => abrirModalPedido('saida')}>
            <MaterialCommunityIcons name="minus-circle-outline" size={22} color="#fff" />
            <Text style={styles.textoBotao}>Retirar produto</Text>
          </TouchableOpacity>
        </View>

        {mensagem !== '' && (
          <Text style={[styles.mensagem, { color: sucesso ? '#86EFAC' : '#FCA5A5' }]}>
            {mensagem}
          </Text>
        )}

        {/* ---- LISTA DE FORNECEDORES ---- */}
        <View style={styles.secaoTitulo}>
          <MaterialCommunityIcons name="truck-delivery-outline" size={22} color="#fff" />
          <Text style={styles.secaoTexto}>Fornecedores</Text>
          <View style={styles.contador}>
            <Text style={styles.contadorTexto}>{fornecedores.length}</Text>
          </View>
        </View>

        {fornecedores.length === 0 ? (
          <Text style={styles.vazio}>
            {erros.fornecedores ? 'Não foi possível carregar os fornecedores.' : 'Nenhum fornecedor cadastrado.'}
          </Text>
        ) : (
          fornecedores.map((f, index) => (
            <View key={f.fornecedor_id ?? `fornecedor-${index}`} style={styles.itemCard}>
              <View style={styles.itemIcone}>
                <MaterialCommunityIcons name="truck-outline" size={24} color="#86EFAC" />
              </View>
              <View style={styles.itemInfo}>
                <Text style={styles.itemNome} numberOfLines={1}>{f.fornecedor_nome}</Text>
                {!!f.fornecedor_tipo_produtos && (
                  <Text style={styles.itemDetalhe} numberOfLines={1}>{f.fornecedor_tipo_produtos}</Text>
                )}
                {!!f.fornecedor_cnpj && (
                  <Text style={styles.itemDetalhe}>CNPJ: {f.fornecedor_cnpj}</Text>
                )}
                {!!f.fornecedor_endereco && (
                  <Text style={styles.itemDetalhe} numberOfLines={2}>{f.fornecedor_endereco}</Text>
                )}
              </View>
            </View>
          ))
        )}

        {/* ---- LISTA DE ANIMAIS ---- */}
        <View style={[styles.secaoTitulo, { marginTop: 28 }]}>
          <MaterialCommunityIcons name="paw" size={22} color="#fff" />
          <Text style={styles.secaoTexto}>Animais</Text>
          <View style={styles.contador}>
            <Text style={styles.contadorTexto}>{animais.length}</Text>
          </View>
        </View>

        {animais.length === 0 ? (
          <Text style={styles.vazio}>
            {erros.animais ? 'Não foi possível carregar os animais.' : 'Nenhum animal cadastrado.'}
          </Text>
        ) : (
          animais.map((a, index) => (
            <View key={a.animal_id ?? a.id ?? `animal-${index}`} style={styles.itemCard}>
              <View style={styles.itemIcone}>
                <MaterialCommunityIcons name="paw" size={24} color="#86EFAC" />
              </View>
              <View style={styles.itemInfo}>
                <Text style={styles.itemNome} numberOfLines={1}>{a.animal_identificacao}</Text>
                <Text style={styles.itemDetalhe} numberOfLines={1}>
                  {[a.animal_especie, a.animal_raca].filter(Boolean).join(' • ')}
                </Text>
                <Text style={styles.itemDetalhe}>
                  {[a.animal_sexo, a.animal_idade != null && a.animal_idade !== '' ? `${a.animal_idade} anos` : null]
                    .filter(Boolean)
                    .join(' • ')}
                </Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>

      {tipoMovimentacao && (
        <ModalPedido
          visible={modalVisible}
          tipo={tipoMovimentacao}
          produtosDisponiveis={produtosFormatados}
          referenciasDisponiveis={referenciasDoModal}
          onClose={() => setModalVisible(false)}
          onConfirmar={enviarPedido}
        />
      )}
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  menu: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 10,
  },
  menuEsquerda: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  logo: {
    width: 60,
    height: 60,
  },
  header: {
    borderBottomColor: '#fff',
    borderBottomWidth: 2,
    paddingBottom: 8,
    marginBottom: 24,
    marginTop: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
  },

  // Diagnóstico
  diagnostico: {
    backgroundColor: 'rgba(0, 0, 0, 0.45)',
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#FCD34D',
  },
  diagnosticoTitulo: {
    color: '#FCD34D',
    fontWeight: 'bold',
    marginBottom: 6,
  },
  diagnosticoLinha: {
    color: '#fff',
    fontSize: 12,
    marginTop: 2,
  },
  diagnosticoDica: {
    color: '#FCD34D',
    fontSize: 12,
    marginTop: 8,
  },

  // Botões
  botoesLinha: {
    flexDirection: 'row',
    gap: 12,
  },
  botao: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#03A64A',
    padding: 15,
    borderRadius: 10,
  },
  botao_saida: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#bd0404',
    padding: 15,
    borderRadius: 10,
  },
  textoBotao: {
    color: '#ffff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  mensagem: {
    marginTop: 16,
    textAlign: 'center',
    fontSize: 15,
    fontWeight: 'bold',
  },

  // Listas
  secaoTitulo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 28,
    marginBottom: 12,
  },
  secaoTexto: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  contador: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 2,
  },
  contadorTexto: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 13,
  },
  itemCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.12)',
    borderRadius: 18,
    padding: 14,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
  },
  itemIcone: {
    width: 48,
    height: 48,
    borderRadius: 14,
    backgroundColor: 'rgba(34, 197, 94, 0.18)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  itemInfo: {
    flex: 1,
  },
  itemNome: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  itemDetalhe: {
    color: '#CBD5E1',
    fontSize: 13,
    marginTop: 3,
  },
  vazio: {
    color: '#ffffffaa',
    textAlign: 'center',
    paddingVertical: 14,
  },
});