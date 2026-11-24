import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Image, RefreshControl } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useState, useEffect } from 'react';
import ModalPedido from './ModalPedido';
import { API_URL } from '../src/services/api';


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

  useEffect(() => {
    carregarProdutos();
    carregarFornecedores();
    carregarAnimais();
  }, []);

  async function carregarProdutos() {
    setCarregandoProdutos(true);
    try {
      const res = await fetch(`${API_URL}/api/produtos`);
      const data = await res.json();
      // LOG TEMPORÁRIO: veja no terminal os nomes reais dos campos (remova depois)
      console.log('PRODUTO[0]:', JSON.stringify(Array.isArray(data) ? data[0] : data));
      if (Array.isArray(data)) {
        setProdutosEstoque(data);
      } else {
        console.log('Resposta inesperada de /api/produtos:', data);
        setProdutosEstoque([]);
      }
    } catch (err) {
      console.log('Erro ao carregar produtos:', err);
      setProdutosEstoque([]);
    } finally {
      setCarregandoProdutos(false);
    }
  }

  async function carregarFornecedores() {
    try {
      const res = await fetch(`${API_URL}/api/fornecedores`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setFornecedores(data);
      } else {
        console.log('Resposta inesperada de /api/fornecedores:', data);
        setFornecedores([]);
      }
    } catch (err) {
      console.log('Erro ao carregar fornecedores:', err);
      setFornecedores([]);
    }
  }

  async function carregarAnimais() {
    try {
      const res = await fetch(`${API_URL}/api/animais`);
      const data = await res.json();
      // LOG TEMPORÁRIO: veja no terminal os nomes reais dos campos (remova depois)
      console.log('ANIMAL[0]:', JSON.stringify(Array.isArray(data) ? data[0] : data));
      if (Array.isArray(data)) {
        setAnimais(data);
      } else {
        console.log('Resposta inesperada de /api/animais:', data);
        setAnimais([]);
      }
    } catch (err) {
      console.log('Erro ao carregar animais:', err);
      setAnimais([]);
    }
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
    nome: f.fornecedor_nome,
    subtitulo: f.fornecedor_tipo_produtos,
  }));

  const animaisFormatados = animais.map((a, i) => ({
    id: a.animal_id ?? a.id ?? i,
    nome: a.animal_identificacao,
    subtitulo: `${a.animal_especie} • ${a.animal_raca}`,
  }));

  // Produtos no formato que o ModalPedido espera ({ id, nome, estoque_quantidade })
  // Se o log "PRODUTO[0]" mostrar outros nomes de campo, ajuste aqui.
  const produtosFormatados = produtosEstoque.map((p, i) => ({
    id: p.produto_id ?? p.id ?? i,
    nome: p.produto_nome ?? p.nome,
    estoque_quantidade: p.estoque_quantidade ?? 0,
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
          <Text style={styles.vazio}>Nenhum fornecedor cadastrado.</Text>
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
          <Text style={styles.vazio}>Nenhum animal cadastrado.</Text>
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