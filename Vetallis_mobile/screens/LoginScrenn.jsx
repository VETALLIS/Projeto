
import { StyleSheet, Text, View, Image, TextInput, TouchableOpacity} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import Checkbox from 'expo-checkbox';
import {useState} from 'react';
import { useNavigation } from '@react-navigation/native';

export default function Login() {
  const [Email, setEmail] = useState('')
  const [Senha, setSenha] = useState('')
  const [mensagem, setMensagem] = useState('')
  const [sucesso, setSucesso] = useState('')
  const [isChecked, setChecked] = useState(false);
  const navigation = useNavigation();
  
  function fazerLogin(){
    if (Email === "teste@gmail.com" && Senha === "123"){
      setMensagem('Login realizado com sucesso!')
      setSucesso(true)
      navigation.replace('App')
    } else {
      setMensagem("Email ou senha invalidas")
      setSucesso(false)
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
          <TouchableOpacity style={styles.botao} onPress={fazerLogin}>
            <Text style={styles.textoBotao}>Entrar</Text>
          </TouchableOpacity>
          {mensagem !== '' && (
            <Text style={[
              styles.mensagem,
              {color:sucesso ? '#2e7d32' : '#d32f2f'}
            ]}>{mensagem}</Text>
          )}
      </View>
      <View style={styles.container}>
        <TouchableOpacity>
          <Text style={styles.textoBotao}>Esqueceu sua senha</Text>
        </TouchableOpacity>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex:1,
    padding: 20,

  },
  card:{
    backgroundColor: '#ffff',
    borderRadius:16,
    padding:25,
    elevation:8,
    shadowColor: '#000',
    shadowOffset: {width:0, height:5},
    shadowRadius: 10,
    height:600,
    width:500,
    alignSelf:'center',
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
  logo: {
    width:  175,
    height: 175,
    resizeMode: 'contain',
    alignSelf: 'center',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#e0e0e0",
    marginBottom: 62,
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
    marginBottom: 62,
  },
  checkbox: {
    alignSelf: 'center',
  },
  label: {
    fontSize: 18,
    margin:8,
    color: '#11686F',
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
  }
});
