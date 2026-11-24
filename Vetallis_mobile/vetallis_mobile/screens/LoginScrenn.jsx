import { StyleSheet, Text, View, TextInput, TouchableOpacity, ActivityIndicator, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import Checkbox from 'expo-checkbox';
import { useState, useEffect } from 'react';
import { useNavigation } from '@react-navigation/native';
import { useAuth } from '../screens/AuthContext';
import { API_URL } from '../src/services/api';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';



export default function Login() {
  const [Email, setEmail] = useState('')
  const [Senha, setSenha] = useState('')
  const [mensagem, setMensagem] = useState('')
  const [sucesso, setSucesso] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [isChecked, setChecked] = useState(false);
  const navigation = useNavigation();
  const { setUsuario } = useAuth();

  useEffect(() => {
    async function carregarDadosSalvos() {
      try {
        const lembrar = await AsyncStorage.getItem('lembrar');
        if (lembrar === 'true') {
          const emailSalvo = await AsyncStorage.getItem('emailSalvo');
          const senhaSalva = await SecureStore.getItemAsync('senhaSalva');
          if (emailSalvo) setEmail(emailSalvo);
          if (senhaSalva) setSenha(senhaSalva);
          setChecked(true);
        }
      } catch (e) {
        console.log('Erro ao carregar dados salvos:', e);
      }
    }
    carregarDadosSalvos();
  }, []);

  async function salvarLembrar() {
    try {
      if (isChecked) {
        await AsyncStorage.setItem('lembrar', 'true');
        await AsyncStorage.setItem('emailSalvo', Email);
        await SecureStore.setItemAsync('senhaSalva', Senha);
        console.log('Lembrar-me salvo:', Email);
      } else {
        await AsyncStorage.multiRemove(['lembrar', 'emailSalvo']);
        await SecureStore.deleteItemAsync('senhaSalva');
      }
    } catch (e) {
      console.log('Erro ao salvar Lembrar-me:', e);
    }
  }

  async function fazerLogin() {
    if (!Email || !Senha) {
      setMensagem('Preencha email e senha');
      setSucesso(false);
      return;
    }

    setCarregando(true);
    setMensagem('');

    try {
      const resposta = await fetch(`${API_URL}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email, senha: Senha }),
      });

      const dados = await resposta.json();

      if (resposta.ok && dados.sucesso) {
        await salvarLembrar();   // 👈 salva ANTES de navegar

        setMensagem('Login realizado com sucesso!');
        setSucesso(true);
        setUsuario(dados.usuario);
        navigation.replace('App');
      } else {
        setMensagem(dados.mensagem || 'Email ou senha inválidos');
        setSucesso(false);
      }
    } catch (erro) {
      setMensagem('Não foi possível conectar ao servidor');
      setSucesso(false);
    } finally {
      setCarregando(false);
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
      {/* Sobe a tela quando o teclado abre */}
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        {/* Se a tela for pequena, dá pra rolar em vez de estourar */}
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <Text style={styles.titulo}>VETALLIS</Text>
          <Text style={styles.subtitulo}>Acesse sua conta</Text>

          <View style={styles.card}>
            <Text style={styles.escrita}>Email</Text>
            <View style={styles.inputContainer}>
              <MaterialCommunityIcons name="email-outline" size={22} color="#999" style={styles.icone} />
              <TextInput
                style={styles.input}
                placeholder='Digite seu email'
                placeholderTextColor="#999"
                value={Email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                editable={!carregando}
              />
            </View>
            <Text style={styles.escrita}>Senha</Text>
            <View style={styles.inputContainer}>
              <Ionicons name="lock-closed-outline" size={22} color="#999" style={styles.icone} />
              <TextInput
                style={styles.input}
                placeholder='Digite sua senha'
                placeholderTextColor="#999"
                value={Senha}
                onChangeText={setSenha}
                secureTextEntry
                editable={!carregando}
              />
            </View>
            <View style={styles.checkrow}>
              <Checkbox
                style={styles.checkbox}
                value={isChecked}
                onValueChange={setChecked}
                color={isChecked ? '#4630EB' : undefined}
              />
              <Text style={styles.label}>Lembrar-me</Text>
            </View>
            <TouchableOpacity style={styles.botao} onPress={fazerLogin} disabled={carregando}>
              {carregando ? (
                <ActivityIndicator color="#ffff" />
              ) : (
                <Text style={styles.textoBotao}>Entrar</Text>
              )}
            </TouchableOpacity>
            {mensagem !== '' && (
              <Text style={[
                styles.mensagem,
                { color: sucesso ? '#2e7d32' : '#d32f2f' }
              ]}>{mensagem}</Text>
            )}
          </View>

          <TouchableOpacity style={styles.linkSenha} onPress={() => navigation.navigate('EsqueceuSenha')}>
            <Text style={styles.textoBotao}>Esqueceu sua senha</Text>
          </TouchableOpacity>
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scroll: {
    flexGrow: 1,
    justifyContent: 'center', // centraliza quando sobra espaço
    padding: 20,
    paddingVertical: 40,
  },
  card: {
    backgroundColor: '#ffff',
    borderRadius: 16,
    padding: 20,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowRadius: 10,
    width: '100%',      // ocupa a largura do celular...
    maxWidth: 500,      // ...mas não passa de 500 (tablet)
    alignSelf: 'center',
  },
  titulo: {
    alignSelf: 'center',
    fontSize: 40,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitulo: {
    alignSelf: 'center',
    fontSize: 20,
    marginBottom: 30,
    color: '#ccc',
  },
  escrita: {
    fontSize: 18,
    marginBottom: 8,
    color: '#116f22',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#e0e0e0",
    marginBottom: 20,
    paddingHorizontal: 10,
  },
  icone: {
    marginRight: 8,
  },
  input: {
    fontSize: 15,
    flex: 1,
    padding: 15,
  },
  checkrow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  checkbox: {
    alignSelf: 'center',
  },
  label: {
    fontSize: 16,
    margin: 8,
    color: '#116f13',
  },
  botao: {
    backgroundColor: "#03A64A",
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 5
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
  linkSenha: {
    marginTop: 25,
    padding: 10,
    alignSelf: 'center',
  },
});