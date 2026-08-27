import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons, FontAwesome } from '@expo/vector-icons';
import { View, Text, StyleSheet, Image, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useState, useEffect } from 'react';
import { useAuth } from '../screens/AuthContext';

// Mesmo IP/porta usados nas outras telas — se você já centralizou isso em
// src/services/api.js, troque essa constante por um import de lá.
const API_URL = 'http://10.135.60.25:3000';

export default function DashScreen() {
    const { usuario } = useAuth();

    const [estoqueTotal, setEstoqueTotal] = useState(0);
    const [produtosDestaque, setProdutosDestaque] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState('');

    async function carregarDados() {
        setCarregando(true);
        setErro('');
        try {
            const [respostaPainel, respostaProdutos] = await Promise.all([
                fetch(`${API_URL}/api/painel`),
                fetch(`${API_URL}/api/produtos`),
            ]);

            const dadosPainel = await respostaPainel.json();
            const dadosProdutos = await respostaProdutos.json();

            if (respostaPainel.ok) {
                setEstoqueTotal(dadosPainel.totalProdutos || 0);
            }

            if (respostaProdutos.ok) {
                // Mostra só os 3 primeiros produtos em destaque
                setProdutosDestaque(dadosProdutos.slice(0, 3));
            }
        } catch (e) {
            setErro('Não foi possível conectar ao servidor.');
        } finally {
            setCarregando(false);
        }
    }

    useEffect(() => {
        carregarDados();
    }, []);

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
                    <Image
                        source={require('../assets/vetallis.png')}
                        style={styles.logo}
                    />
                </View>
                <View style={styles.menuDireita}>
                    <View style={styles.iconCircle}>
                        <MaterialCommunityIcons name="magnify" size={30} color="#fefefe" />
                    </View>
                    <TouchableOpacity style={styles.iconCircle} onPress={carregarDados}>
                        <MaterialCommunityIcons name="refresh" size={30} color="#fefefe" />
                    </TouchableOpacity>
                </View>
            </View>

            <View style={styles.header}>
                <View>
                    <FontAwesome name="user" size={50} color="white" style={styles.icone_pessoa} />
                </View>
                <View>
                    <Text style={styles.title}>
                        Bem-vindo
                    </Text>
                    <Text style={styles.subtitulo}>
                        {usuario?.nome || 'Usuário'}
                    </Text>
                </View>
            </View>

            {erro !== '' && (
                <Text style={styles.mensagemErro}>{erro}</Text>
            )}

            <View style={styles.card}>
                <View>
                    <View style={styles.card_menor}>
                        <Text style={styles.letra}>Temperatura</Text>
                        <Text style={styles.fundo}>2 *C</Text>
                    </View>
                    <View style={styles.card_menor}>
                        <Text style={styles.letra}>Luminosidade</Text>
                        <Text style={styles.fundo}>300 lux</Text>
                    </View>
                </View>
                <View>
                    <View style={styles.card_menor}>
                        <Text style={styles.letra}>Estoque total</Text>
                        {carregando ? (
                            <ActivityIndicator color="#000" />
                        ) : (
                            <Text style={styles.fundo}>{estoqueTotal} unidades</Text>
                        )}
                    </View>
                    <View style={styles.card_menor}>
                        <Text style={styles.letra}>Umidade</Text>
                        <Text style={styles.fundo}>20%</Text>
                    </View>
                </View>
            </View>
            <View style={styles.card_alerta}>
                <View style={styles.alerta}>
                    <Text style={styles.alerta_titulo}>Alertas</Text>
                    <Text style={styles.alerta_titulo}>  Ver detalhes </Text>
                </View>
                <View style={styles.alerta_espaço}>
                    <View>
                        <FontAwesome name="thermometer" size={50} color="white" style={styles.icone_pessoa} />
                    </View>
                    <View >
                        <Text style={styles.alerta_subtitulo}>
                            Temperatura acima do ideal
                        </Text>
                        <Text style={styles.alerta_subtitulo}>
                            Câmera 1 - 15 graus
                        </Text>
                    </View>
                </View>

            </View>
            <View style={styles.card_produtos}>
                <Text style={styles.alerta_titulo}>
                    Produtos em Destaque
                </Text>
                {carregando ? (
                    <ActivityIndicator color="#fff" style={{ marginTop: 15 }} />
                ) : produtosDestaque.length === 0 ? (
                    <Text style={styles.alerta_subtitulo}>Nenhum produto cadastrado.</Text>
                ) : (
                    <View style={styles.ajuste}>
                        {produtosDestaque.map((produto) => (
                            <View key={produto.id} style={styles.card_produto}>
                                <Image
                                    source={
                                        produto.temImagem
                                            ? { uri: `${API_URL}/api/produtos/${produto.id}/imagem` }
                                            : require('../assets/vetallis.png')
                                    }
                                    style={styles.logo}
                                />
                                <Text style={styles.letra_produtos} numberOfLines={1}>
                                    {produto.nome}
                                </Text>
                                <Text style={styles.fundo_produto}>
                                    {produto.quantidade} un.
                                </Text>
                            </View>
                        ))}
                    </View>
                )}
            </View>
        </LinearGradient>

    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,

    },
    card: {
        backgroundColor: 'rgba(255, 255, 255, 0.28)',
        borderRadius: 15,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
        width: '100%',
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 5
    },
    card_menor: {
        backgroundColor: '#ffffff',
        borderRadius: 15,
        padding: 15,
        margin: 15,
    },
    titulo: {
        alignSelf: 'center',
        fontSize: 15,
        fontWeight: 'bold',
        color: '#fff',
    },
    subtitulo: {
        alignSelf: 'center',
        fontSize: 28,
        marginBottom: 52,
        color: '#ccc',
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
        marginTop: 20,
        marginBottom: 15,
        flexDirection: 'row',
        alignItems: 'center',
    },

    title: {
        color: '#fff',
        fontSize: 25,
        fontWeight: 'bold',
    },
    imagem: {
        width: 400,
        height: 400,
        alignSelf: 'center'
    },
    letra: {
        color: '#000000',
        fontSize: 20,
        fontWeight: 'bold',
        padding: 5
    },
    fundo: {
        color: '#000000',
        fontSize: 20,
        fontWeight: 'bold',
        backgroundColor: '#0ee83298',
        borderRadius: 5,
        padding: 7,
    },
    alerta: {
        borderBottomColor: '#fff',
        borderBottomWidth: 2,   // <-- adiciona isso
        paddingBottom: 8,
        marginBottom: 20,
        marginTop: 20,
        flexDirection: 'row',
        justifyContent: 'space-between'
    },
    alerta_titulo: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
        padding: 5
    },
    card_alerta: {
        backgroundColor: 'rgba(255, 255, 255, 0.28)',
        borderRadius: 15,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
        width: '100%',
        justifyContent: 'space-between',
        marginBottom: 5
    },
    alerta_espaço: {
        flexDirection: 'row'
    },
    alerta_subtitulo: {
        fontsize: 18,
        marginLeft: 10,
        color: '#fff',
    },
    ajuste: {
        flexDirection: 'row'
    },
    card_produtos: {
        backgroundColor: 'rgba(255, 255, 255, 0.28)',
        borderRadius: 15,
        padding: 25,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
        marginBottom: 5
    },
    letra_produtos: {
        color: '#000000',
        fontSize: 15,
        fontWeight: 'bold',
        padding: 5,
        maxWidth: 90,
    },
    fundo_produto: {
        color: '#0f5d1c98',
        fontSize: 12,
        fontWeight: 'bold',
        backgroundColor: '#0ab82798',
        borderRadius: 5,
        marginLeft: 3

    },
    mensagemErro: {
        color: '#fff',
        textAlign: 'center',
        marginBottom: 10,
        fontSize: 14,
    },
    card_produto: {
        backgroundColor: '#ffffff',
        borderRadius: 15,
        padding: 15,
        margin: 15,
        width: '30%',
        alignItems: 'center'
    },
});