import { StyleSheet, Text, View, ScrollView, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useState } from 'react';
import { CameraView, useCameraPermissions } from 'expo-camera';

export default function LeitorScreen() {
  const [mensagem, setMensagem] = useState('');
  const [sucesso, setSucesso] = useState('');
  const [scanning, setScanning] = useState(false);
  const [scannedData, setScannedData] = useState(null);
  const [permission, requestPermission] = useCameraPermissions();

  function movimentacao() {
    setMensagem('Movimentação realizada com sucesso');
    setSucesso(true);
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

          <TouchableOpacity style={styles.botao} onPress={movimentacao}>
            <Text style={styles.textoBotao}>Adicionar produto</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.botao_saida} onPress={movimentacao}>
            <Text style={styles.textoBotao}>Retirar produto</Text>
          </TouchableOpacity>

          {mensagem !== '' && (
            <Text style={[styles.mensagem, { color: sucesso ? '#2e7d32' : '#d32f2f' }]}>
              {mensagem}
            </Text>
          )}
        </View>
      </ScrollView>
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
    width: '100%',        // era 500
    alignSelf: 'center',
    paddingTop: 25,
  },
  iconBox: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f2f2f2',
    borderRadius: 16,
    paddingVertical: 40,
    minHeight: 250
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
    borderColor: "#e0e0e0",
  },
  menu: {
    flexDirection: 'row',
    justifyContent: 'space-between',  // empurra esquerda e direita
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
    backgroundColor: 'rgba(255, 255, 255, 0.15)',  // translúcido
    justifyContent: 'center',
    alignItems: 'center',
  },
  logo: {
    width: 60,
    height: 60,
  },
  header: {
    marginTop: 55,
    marginBottom: 25,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  title: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
  },
  header: {
    borderBottomColor: '#fff',
    borderBottomWidth: 2,   // <-- adiciona isso
    paddingBottom: 8,
    marginBottom: 50,
    marginTop: 20,
  },
  imagem: {
    width: 400,
    height: 400,
    alignSelf: 'center'
  },
  botao: {
    backgroundColor: "#03A64A",
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 40
  },
  textoBotao: {
    color: "#ffff",
    fontWeight: 'bold',
    fontSize: 16,
    alignSelf: 'center',
  },
  mensagem: {
    marginTop: 20,
    textAlign: 'center',
    fontSize: 15,
    fontWeight: 'bold'
  },
  botao_saida: {
    backgroundColor: "#bd0404",
    marginTop: 15,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 50
  },
});
