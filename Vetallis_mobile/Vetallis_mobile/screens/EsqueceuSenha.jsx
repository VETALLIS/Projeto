import { StyleSheet, Text, View, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialCommunityIcons, Ionicons } from '@expo/vector-icons';
import { useState } from 'react';
import { useNavigation } from '@react-navigation/native';
import { API_URL } from '../src/services/api';

export default function EsqueceuSenha() {
    const [etapa, setEtapa] = useState(1); // 1 = digitar email, 2 = nova senha
    const [email, setEmail] = useState('');
    const [novaSenha, setNovaSenha] = useState('');
    const [confirmarSenha, setConfirmarSenha] = useState('');
    const [mensagem, setMensagem] = useState('');
    const [sucesso, setSucesso] = useState(false);
    const [carregando, setCarregando] = useState(false);
    const navigation = useNavigation();

    async function verificarEmail() {
        if (!email) {
            setMensagem('Digite seu email');
            setSucesso(false);
            return;
        }
        setCarregando(true);
        setMensagem('');
        try {
            const resposta = await fetch(`${API_URL}/api/esqueci-senha`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email }),
            });
            const dados = await resposta.json();
            if (resposta.ok && dados.sucesso) {
                setEtapa(2);
                setMensagem('');
            } else {
                setMensagem(dados.mensagem || 'Email não encontrado');
                setSucesso(false);
            }
        } catch (erro) {
            setMensagem('Não foi possível conectar ao servidor');
            setSucesso(false);
        } finally {
            setCarregando(false);
        }
    }

    async function redefinirSenha() {
        if (!novaSenha || !confirmarSenha) {
            setMensagem('Preencha os dois campos de senha');
            setSucesso(false);
            return;
        }
        if (novaSenha !== confirmarSenha) {
            setMensagem('As senhas não coincidem');
            setSucesso(false);
            return;
        }
        setCarregando(true);
        setMensagem('');
        try {
            const resposta = await fetch(`${API_URL}/api/redefinir-senha`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, novaSenha }),
            });
            const dados = await resposta.json();
            if (resposta.ok && dados.sucesso) {
                setMensagem('Senha redefinida! Faça login.');
                setSucesso(true);
                setTimeout(() => navigation.goBack(), 1500);
            } else {
                setMensagem(dados.mensagem || 'Erro ao redefinir senha');
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
            <Text style={styles.titulo}>VETALLIS</Text>
            <Text style={styles.subtitulo}>
                {etapa === 1 ? 'Recuperar senha' : 'Nova senha'}
            </Text>

            <View style={styles.card}>
                {etapa === 1 ? (
                    <>
                        <Text style={styles.escrita}>Email</Text>
                        <View style={styles.inputContainer}>
                            <MaterialCommunityIcons name="email-outline" size={22} color="#999" style={styles.icone} />
                            <TextInput
                                style={styles.input}
                                placeholder="Digite seu email cadastrado"
                                placeholderTextColor="#999"
                                value={email}
                                onChangeText={setEmail}
                                autoCapitalize="none"
                                keyboardType="email-address"
                                editable={!carregando}
                            />
                        </View>
                        <TouchableOpacity style={styles.botao} onPress={verificarEmail} disabled={carregando}>
                            {carregando ? <ActivityIndicator color="#fff" /> : <Text style={styles.textoBotao}>Continuar</Text>}
                        </TouchableOpacity>
                    </>
                ) : (
                    <>
                        <Text style={styles.escrita}>Nova senha</Text>
                        <View style={styles.inputContainer}>
                            <Ionicons name="lock-closed-outline" size={22} color="#999" style={styles.icone} />
                            <TextInput
                                style={styles.input}
                                placeholder="Digite a nova senha"
                                placeholderTextColor="#999"
                                value={novaSenha}
                                onChangeText={setNovaSenha}
                                secureTextEntry
                                editable={!carregando}
                            />
                        </View>
                        <Text style={styles.escrita}>Confirmar senha</Text>
                        <View style={styles.inputContainer}>
                            <Ionicons name="lock-closed-outline" size={22} color="#999" style={styles.icone} />
                            <TextInput
                                style={styles.input}
                                placeholder="Confirme a nova senha"
                                placeholderTextColor="#999"
                                value={confirmarSenha}
                                onChangeText={setConfirmarSenha}
                                secureTextEntry
                                editable={!carregando}
                            />
                        </View>
                        <TouchableOpacity style={styles.botao} onPress={redefinirSenha} disabled={carregando}>
                            {carregando ? <ActivityIndicator color="#fff" /> : <Text style={styles.textoBotao}>Redefinir senha</Text>}
                        </TouchableOpacity>
                    </>
                )}

                {mensagem !== '' && (
                    <Text style={[styles.mensagem, { color: sucesso ? '#2e7d32' : '#d32f2f' }]}>{mensagem}</Text>
                )}
            </View>

            <TouchableOpacity onPress={() => navigation.goBack()}>
                <Text style={styles.voltar}>Voltar ao login</Text>
            </TouchableOpacity>
        </LinearGradient>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    card: {
        backgroundColor: '#fff',
        borderRadius: 16,
        padding: 25,
        marginTop: 35,
        elevation: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 5 },
        shadowRadius: 10,
        alignSelf: 'center',
        width: '100%',
        maxWidth: 500,
    },
    titulo: { 
        alignSelf: 'center', 
        fontSize: 50, 
        marginTop: 20, 
        fontWeight: 'bold', 
        color: '#fff' 
    },
    subtitulo: { 
        alignSelf: 'center',
        fontSize: 24, 
        marginBottom: 30, 
        color: '#ccc' 
    },
    escrita: { 
        fontSize: 20, 
        marginBottom: 10, 
        color: '#116f22' 
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#e0e0e0',
        marginBottom: 24,
        paddingHorizontal: 10,
    },
    icone: { 
        marginRight: 8
    },
    input: { 
        fontSize: 15,
        flex: 1, 
        padding: 15 
    },
    botao: { 
        backgroundColor: '#03A64A', 
        padding: 15, 
        borderRadius: 10, 
        alignItems: 'center', 
        marginTop: 5 
    },
    textoBotao: { 
        color: '#fff', 
        fontWeight: 'bold', 
        fontSize: 16, 
        alignSelf: 'center' 
    },
    mensagem: { 
        marginTop: 20, 
        textAlign: 'center', 
        fontSize: 15, 
        fontWeight: 'bold' 
    },
    voltar: { 
        color: '#ccc', 
        textAlign: 'center', 
        marginTop: 20, 
        fontSize: 15 
    }
});