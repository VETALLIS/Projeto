import { StyleSheet, Text, View, ScrollView, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useState, useEffect } from 'react';
import { CameraView, useCameraPermissions } from 'expo-camera';
import ModalPedido from './ModalPedido';

const API_URL = 'http://10.135.60.25:3000';

export default function LeitorScreen() {
  const [mensagem, setMensagem] = useState('');
  const [sucesso, setSucesso] = useState('');
  const [scanning, setScanning] = useState(false);
  const [scannedData, setScannedData] = useState(null);
  const [permission, requestPermission] = useCameraPermissions();

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
      setProdutosEstoque(data);
    } catch (err) {
      console.log('Erro ao carregar produtos:', err);
    } finally {
      setCarregandoProdutos(false);
    }
  }

  async function carregarFornecedores() {
    try {
      const res = await fetch(`${API_URL}/api/fornecedores`);
      const data = await res.json();
      setFornecedores(data);
    } catch (err) {
      console.log('Erro ao carregar fornecedores:', err);
    }
  }

  async function carregarAnimais() {
    try {
      const res = await fetch(`${API_URL}/api/animais`);
      const data = await res.json();
      setAnimais(data);
    } catch (err) {
      console.log('Erro ao carregar animais:', err);
    }
  }

  // Listas já formatadas pro formato que o ModalPedido espera ({ id, nome, subtitulo })
  const fornecedoresFormatados = fornecedores.map((f) => ({
    id: f.fornecedor_id,
    nome: f.fornecedor_nome,
    subtitulo: f.fornecedor_tipo_produtos,
  }));

  const animaisFormatados = animais.map((a) => ({
    id: a.animal_id,
    nome: a.animal_identificacao,
    subtitulo: `${a.animal_especie} • ${a.animal_raca}`,
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

  async function abrirLeitor() {
    if (!permission?.granted) {
      const res = await requestPermission();
      if (!res.granted) {
        setMensagem('Permissão de câmera negada');
        setSucesso(false);
        return;
      }
    }
    setScannedData(null);
    setScanning(true);
  }

  function handleBarcodeScanned({ data }) {
    setScanning(false);
    setScannedData(data);
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
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="calendar-today" size={30} color="#fefefe" />
          </View>
        </View>
        <View style={styles.menuDireita}>
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="magnify" size={30} color="#fefefe" />
          </View>
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="cog-outline" size={30} color="#fefefe" />
          </View>
        </View>
      </View>

      <View style={styles.header}>
        <Text style={styles.title}>Movimentação de produtos</Text>
      </View>

      <ScrollView contentContainerStyle={{ paddingBottom: 30 }} showsVerticalScrollIndicator={false}>
        <View style={styles.card}>
          {scanning ? (
            <View style={styles.cameraBox}>
              <CameraView
                style={StyleSheet.absoluteFillObject}
                barcodeScannerSettings={{ barcodeTypes: ['qr'] }}
                onBarcodeScanned={handleBarcodeScanned}
              />
              <TouchableOpacity style={styles.botao_saida} onPress={() => setScanning(false)}>
                <Text style={styles.textoBotao}>Cancelar</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <View style={styles.iconBox}>
              <MaterialCommunityIcons name="qrcode-scan" size={100} color="#11686F" />
              {scannedData && (
                <Text style={styles.escrita}>Código lido: {scannedData}</Text>
              )}
            </View>
          )}

          <TouchableOpacity style={styles.botao} onPress={abrirLeitor}>
            <Text style={styles.textoBotao}>
              {scanning ? 'Escaneando...' : 'Escanear QR Code'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.botao} onPress={() => abrirModalPedido('entrada')}>
            <Text style={styles.textoBotao}>Adicionar produto</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.botao_saida} onPress={() => abrirModalPedido('saida')}>
            <Text style={styles.textoBotao}>Retirar produto</Text>
          </TouchableOpacity>

          {mensagem !== '' && (
            <Text style={[styles.mensagem, { color: sucesso ? '#2e7d32' : '#d32f2f' }]}>
              {mensagem}
            </Text>
          )}
        </View>
      </ScrollView>

      {tipoMovimentacao && (
        <ModalPedido
          visible={modalVisible}
          tipo={tipoMovimentacao}
          produtosDisponiveis={produtosEstoque}
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
  card: {
    backgroundColor: '#ffffffd5',
    borderRadius: 25,
    padding: 25,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowRadius: 10,
    width: '100%',
    alignSelf: 'center',
    paddingTop: 25,
  },
  iconBox: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f2f2f2',
    borderRadius: 16,
    paddingVertical: 40,
    minHeight: 250,
  },
  titulo: {
    alignSelf: 'center',
    fontSize: 50,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitulo: {
    alignSelf: 'center',
    fontSize: 28,
    marginBottom: 52,
    color: '#ccc',
  },
  escrita: {
    fontSize: 25,
    marginBottom: 20,
    color: '#11686F',
  },
  icone: {
    marginRight: 8,
  },
  input: {
    fontSize: 15,
    flex: 1,
    padding: 15,
    borderColor: '#e0e0e0',
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
  menuDireita: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  iconCircle: {
    width: 50,
    height: 50,
    borderRadius: 21,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  logo: {
    width: 60,
    height: 60,
  },
  header: {
    borderBottomColor: '#fff',
    borderBottomWidth: 2,
    paddingBottom: 8,
    marginBottom: 50,
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
  imagem: {
    width: 400,
    height: 400,
    alignSelf: 'center',
  },
  botao: {
    backgroundColor: '#03A64A',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 40,
  },
  textoBotao: {
    color: '#ffff',
    fontWeight: 'bold',
    fontSize: 16,
    alignSelf: 'center',
  },
  mensagem: {
    marginTop: 20,
    textAlign: 'center',
    fontSize: 15,
    fontWeight: 'bold',
  },
  botao_saida: {
    backgroundColor: '#bd0404',
    marginTop: 50,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
});