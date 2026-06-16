import { StyleSheet, Text, View, Image, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useState } from 'react';

export default function Perfil() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [cargo, setCargo] = useState('');
  const [alterarEmail, setAlterarEmail] = useState('');
  const [alterarNome, setAlterarNome] = useState('');
  const [mudarSenha, setMudarSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  
  const [mensagem, setMensagem] = useState('');
  const [sucesso, setSucesso] = useState(false);

  function salvarAlteracoes() {
    setMensagem('Alterações realizadas com sucesso!');
    setSucesso(true);
  }

  function excluirConta() {
    setMensagem('Conta excluída com sucesso.');
    setSucesso(false);
  }

  return (
    <LinearGradient
      colors={['#000000', '#0d3b2e', '#0a4a3a', '#1a6b4a']}
      locations={[0, 0.3, 0.6, 1]}
      start={{ x: 0.2, y: 0.1 }}
      end={{ x: 1, y: 1 }}
      style={styles.container}
    >
      {/* HEADER / BARRA SUPERIOR */}
      <View style={styles.menu}>
        <View style={styles.menuEsquerda}>
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="calendar-today" size={26} color="#fefefe" />
          </View>
          <Image
            source={require('../assets/vetallis.png')}
            style={styles.logo}
          />
        </View>
        <View style={styles.menuDireita}>
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="magnify" size={40} color="#fefefe" />
          </View>
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="cog-outline" size={26} color="#fefefe" />
          </View>
        </View>
      </View>

      <View style={styles.header}>
        <Text style={styles.title}>Gerenciamento de perfil</Text>
      </View>


      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 40 }}>
        <View style={styles.card}>
          
          
          <View style={styles.perfilRow}>
            <View style={styles.frameDashed}>
              <MaterialCommunityIcons name="account" size={80} color="#9e9e9e" />
            </View>
            
            <View style={styles.dadosLaterais}>
              <TextInput 
                style={styles.inputLinha} 
                placeholder="Nome" 
                placeholderTextColor="#999"
                value={nome}
                onChangeText={setNome}
              />
              <TextInput 
                style={styles.inputLinha} 
                placeholder="Email" 
                placeholderTextColor="#999"
                value={email}
                onChangeText={setEmail}
              />
              <TextInput 
                style={styles.inputLinha} 
                placeholder="Cargo" 
                placeholderTextColor="#999"
                value={cargo}
                onChangeText={setCargo}
              />
            </View>
          </View>

          
          <View style={styles.inputGrandeContainer}>
            <TextInput 
              style={styles.inputGrande} 
              placeholder="Alterar email" 
              placeholderTextColor="#999"
              value={alterarEmail}
              onChangeText={setAlterarEmail}
            />
          </View>

          <View style={styles.inputGrandeContainer}>
            <TextInput 
              style={styles.inputGrande} 
              placeholder="Alterar nome" 
              placeholderTextColor="#999"
              value={alterarNome}
              onChangeText={setAlterarNome}
            />
          </View>

          
          <View style={styles.senhaRow}>
            <View style={[styles.inputGrandeContainer, { flex: 1, marginRight: 10 }]}>
              <TextInput 
                style={styles.inputGrande} 
                placeholder="Alterar Cargo" 
                placeholderTextColor="#999"
                secureTextEntry
                value={mudarSenha}
                onChangeText={setMudarSenha}
              />
            </View>
            <View style={[styles.inputGrandeContainer, { flex: 1 }]}>
              <TextInput 
                style={styles.inputGrande} 
                placeholder="Confirmar Cargo" 
                placeholderTextColor="#999"
                secureTextEntry
                value={confirmarSenha}
                onChangeText={setConfirmarSenha}
              />
            </View>
          </View>

         
          <TouchableOpacity style={styles.botaoSalvar} onPress={salvarAlteracoes}>
            <View style={styles.btnContent}>
              <MaterialCommunityIcons name="trash-can-outline" size={20} color="#fff" style={{marginRight: 5}} />
              <Text style={styles.textoBotao}>salvar alterações</Text>
            </View>
          </TouchableOpacity>

          <TouchableOpacity style={styles.botaoExcluir} onPress={excluirConta}>
            <View style={styles.btnContent}>
              <Ionicons name="checkmark-circle-outline" size={20} color="#fff" style={{marginRight: 5}} />
              <Text style={styles.textoBotao}>excluir conta</Text>
            </View>
          </TouchableOpacity>

          {mensagem !== '' && (
            <Text style={[
              styles.mensagem,
              { color: sucesso ? '#2e7d32' : '#d32f2f' }
            ]}>{mensagem}</Text>
          )}

        </View>
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 40,
    
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
    borderRadius: 22,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  logo: {
    width: 70,
    height: 70,
    resizeMode: 'contain',
  },
  header: {
    borderBottomColor: 'rgba(255, 255, 255, 0.6)',
    borderBottomWidth: 1,
    paddingBottom: 12,
    marginBottom: 25,
    marginTop: 25,
  },
  title: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
  },
  card: {
    backgroundColor: '#F5F5F5',
    borderRadius: 35,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 6,
    width: '100%',
    height: 800,
  },
  perfilRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 25,
    justifyContent: 'space-between'
  },
  frameDashed: {
    width: 130,
    height: 130,
    borderWidth: 2,
    borderStyle: 'dashed',
    borderColor: '#737171',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#E0E0E0'
  },
  dadosLaterais: {
    flex: 1,
    marginLeft: 20,
    justifyContent: 'center',
  },
  inputLinha: {
    borderBottomWidth: 1,
    borderBottomColor: '#A0A0A0',
    fontSize: 18,
    paddingVertical: 4,
    marginBottom: 25,
    color: '#333',
  },
  inputGrandeContainer: {
    backgroundColor: '#FFF',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#E0E0E0',
    marginBottom: 15,
    paddingHorizontal: 15,
    height: 70,
    justifyContent: 'center',
    elevation: 1,
  },
  inputGrande: {
    fontSize: 15,
    color: '#333',
  },
  senhaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  botaoSalvar: {
    backgroundColor: "#03A64A",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 10,
  },
  botaoExcluir: {
    backgroundColor: "#D32F2F",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 12,
  },
  btnContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center'
  },
  textoBotao: {
    color: "#ffffff",
    fontWeight: 'bold',
    fontSize: 20,
  },
  mensagem: {
    marginTop: 15,
    textAlign: 'center',
    fontSize: 20,
    fontWeight: 'bold',
  },
});
