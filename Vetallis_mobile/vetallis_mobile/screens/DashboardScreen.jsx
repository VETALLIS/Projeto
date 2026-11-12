import { LinearGradient } from 'expo-linear-gradient';
import { MaterialCommunityIcons, FontAwesome } from '@expo/vector-icons';
import {
    View, Text, StyleSheet, Image, TouchableOpacity,
    ActivityIndicator, ScrollView, RefreshControl,
    LayoutAnimation, Platform, UIManager,
} from 'react-native';
import { useState, useEffect } from 'react';
import { useAuth } from '../screens/AuthContext';
import { API_URL } from '../src/services/api';

const IOT_URL = API_URL.replace(/:\d+$/, ':8000');

// Habilita a animação de expandir no Android
if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
    UIManager.setLayoutAnimationEnabledExperimental(true);
}

// Busca a última leitura de um sensor (mesma lógica da versão web)
async function ultimaLeitura(sensor) {
    try {
        const resp = await fetch(`${IOT_URL}/leituras?sensor=${sensor}&limite=1`);
        if (!resp.ok) return null;
        const dados = await resp.json();
        return dados.leituras && dados.leituras.length > 0 ? dados.leituras[0] : null;
    } catch (e) {
        return null;
    }
}

// Arredonda para 1 casa decimal e trata valores vazios
const arredondar = (v) =>
    v === null || v === undefined || isNaN(Number(v))
        ? null
        : Math.round(Number(v) * 10) / 10;

// Card branco com título e valor em selo verde
function CardInfo({ titulo, valor, carregando }) {
    return (
        <View style={styles.card_menor}>
            <Text style={styles.letra}>{titulo}</Text>
            {carregando ? (
                <ActivityIndicator color="#000" />
            ) : (
                <Text style={styles.fundo}>{valor}</Text>
            )}
        </View>
    );
}

// Linha de alerta com ícone e duas linhas de texto
function ItemAlerta({ alerta }) {
    return (
        <View style={styles.alerta_espaco}>
            <FontAwesome name={alerta.icone} size={36} color={alerta.cor || 'white'} style={styles.icone_alerta} />
            <View style={styles.alerta_textos}>
                <Text style={styles.alerta_subtitulo}>{alerta.titulo}</Text>
                <Text style={styles.alerta_subtitulo}>{alerta.detalhe}</Text>
            </View>
        </View>
    );
}

// Card de produto com fallback caso a imagem não carregue
function CardProduto({ produto }) {
    const [erroImagem, setErroImagem] = useState(false);
    const usarImagemDoProduto = produto.temImagem && !erroImagem;

    return (
        <View style={styles.card_produto}>
            <Image
                source={
                    usarImagemDoProduto
                        ? { uri: `${API_URL}/api/produtos/${produto.id}/imagem` }
                        : require('../assets/vetallis.png')
                }
                style={styles.imagem_produto}
                resizeMode={usarImagemDoProduto ? 'cover' : 'contain'}
                onError={() => setErroImagem(true)}
            />
            <Text style={styles.letra_produtos} numberOfLines={1}>
                {produto.nome}
            </Text>
            <Text style={styles.fundo_produto}>{produto.quantidade} un.</Text>
        </View>
    );
}

export default function DashScreen() {
    const { usuario } = useAuth();

    const [estoqueTotal, setEstoqueTotal] = useState(0);
    const [produtosDestaque, setProdutosDestaque] = useState([]);
    // Valores dos sensores vindos da API IoT (FastAPI)
    const [sensores, setSensores] = useState({ temperatura: null, luminosidade: null, umidade: null });
    // Alertas de estoque vindos da API (/api/alertas)
    const [alertas, setAlertas] = useState([]);
    const [mostrarTodos, setMostrarTodos] = useState(false);
    const [carregando, setCarregando] = useState(true);
    const [atualizando, setAtualizando] = useState(false);
    const [erro, setErro] = useState('');

    // Busca DHT11 (temperatura/umidade) e LDR (luminosidade)
    async function carregarSensores() {
        const [dht, ldr] = await Promise.all([
            ultimaLeitura('DHT11'),
            ultimaLeitura('LDR'),
        ]);

        setSensores({
            temperatura: arredondar(dht?.temperatura),
            umidade: arredondar(dht?.umidade),
            luminosidade: arredondar(ldr?.luminosidade),
        });
    }

    async function carregarDados() {
        setErro('');
        try {
            carregarSensores();

            const [painel, produtos, alertasResp] = await Promise.allSettled([
                fetch(`${API_URL}/api/painel`),
                fetch(`${API_URL}/api/produtos`),
                fetch(`${API_URL}/api/alertas`),
            ]);

            let algumaFalha = false;

            if (painel.status === 'fulfilled' && painel.value.ok) {
                const dadosPainel = await painel.value.json();
                setEstoqueTotal(dadosPainel.totalProdutos || 0);
            } else {
                algumaFalha = true;
            }

            if (produtos.status === 'fulfilled' && produtos.value.ok) {
                const dadosProdutos = await produtos.value.json();
                setProdutosDestaque(dadosProdutos.slice(0, 3));
            } else {
                algumaFalha = true;
            }

            if (alertasResp.status === 'fulfilled' && alertasResp.value.ok) {
                const dadosAlertas = await alertasResp.value.json();
                setAlertas(dadosAlertas);
            } else {
                algumaFalha = true;
            }

            if (algumaFalha) {
                setErro('Alguns dados não puderam ser carregados.');
            }
        } catch (e) {
            setErro('Não foi possível conectar ao servidor.');
        } finally {
            setCarregando(false);
            setAtualizando(false);
        }
    }

    useEffect(() => {
        carregarDados();
    }, []);

    // Atualiza os sensores a cada 5 segundos (como na versão web)
    useEffect(() => {
        carregarSensores();
        const intervalo = setInterval(carregarSensores, 5000);
        return () => clearInterval(intervalo);
    }, []);

    function aoPuxarParaAtualizar() {
        setAtualizando(true);
        carregarDados();
    }

    const formatar = (valor, unidade) => (valor === null ? '--' : `${valor} ${unidade}`);

    // Mostra 3 alertas por padrão; "Ver todos" abre a lista completa
    const LIMITE_ALERTAS = 3;
    const alertasVisiveis = mostrarTodos ? alertas : alertas.slice(0, LIMITE_ALERTAS);
    const temMaisAlertas = alertas.length > LIMITE_ALERTAS;

    // Toque no card de alertas: expande para mostrar todos / recolhe para 3
    function alternarAlertas() {
        LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
        setMostrarTodos(!mostrarTodos);
    }

    return (
        <LinearGradient
            colors={['#000000', '#0d3b2e', '#0a4a3a', '#1a6b4a']}
            locations={[0, 0.3, 0.6, 1]}
            start={{ x: 0.2, y: 0.1 }}
            end={{ x: 1, y: 1 }}
            style={styles.container}
        >
            <ScrollView
                contentContainerStyle={styles.conteudo}
                showsVerticalScrollIndicator={false}
                refreshControl={
                    <RefreshControl
                        refreshing={atualizando}
                        onRefresh={aoPuxarParaAtualizar}
                        tintColor="#fff"
                    />
                }
            >
                <View style={styles.menu}>
                    <Image source={require('../assets/vetallis.png')} style={styles.logo} />
                    <TouchableOpacity
                        style={styles.iconCircle}
                        onPress={() => { setCarregando(true); carregarDados(); }}
                        accessibilityLabel="Atualizar dados"
                    >
                        <MaterialCommunityIcons name="refresh" size={30} color="#fefefe" />
                    </TouchableOpacity>
                </View>

                <View style={styles.header}>
                    <FontAwesome name="user" size={50} color="white" style={styles.icone_pessoa} />
                    <View>
                        <Text style={styles.title}>Bem-vindo</Text>
                        <Text style={styles.subtitulo}>{usuario?.nome || 'Usuário'}</Text>
                    </View>
                </View>

                {erro !== '' && <Text style={styles.mensagemErro}>{erro}</Text>}

                <View style={styles.card}>
                    <CardInfo titulo="Temperatura" valor={formatar(sensores.temperatura, '°C')} />
                    <CardInfo titulo="Luminosidade" valor={formatar(sensores.luminosidade, '%')} />
                    <CardInfo
                        titulo="Estoque total"
                        valor={`${estoqueTotal} ${estoqueTotal === 1 ? 'unidade' : 'unidades'}`}
                        carregando={carregando}
                    />
                    <CardInfo titulo="Umidade" valor={formatar(sensores.umidade, '%')} />
                </View>

                <TouchableOpacity
                    activeOpacity={0.85}
                    disabled={!temMaisAlertas}
                    onPress={alternarAlertas}
                    style={styles.card_alerta}
                    accessibilityRole="button"
                    accessibilityLabel={mostrarTodos ? 'Recolher alertas' : 'Expandir e ver todos os alertas'}
                >
                    <View style={styles.alerta}>
                        <Text style={styles.alerta_titulo}>Alertas</Text>
                        {temMaisAlertas && (
                            <View style={styles.alerta_acao}>
                                <Text style={styles.alerta_titulo}>
                                    {mostrarTodos ? 'Ver menos' : `Ver todos (${alertas.length})`}
                                </Text>
                                <FontAwesome
                                    name={mostrarTodos ? 'chevron-up' : 'chevron-down'}
                                    size={14}
                                    color="#fff"
                                />
                            </View>
                        )}
                    </View>

                    {carregando ? (
                        <ActivityIndicator color="#fff" />
                    ) : alertasVisiveis.length === 0 ? (
                        <Text style={styles.texto_vazio}>Nenhum alerta no momento.</Text>
                    ) : (
                        alertasVisiveis.map((alerta) => <ItemAlerta key={alerta.id} alerta={alerta} />)
                    )}
                </TouchableOpacity>

                <View style={styles.card_produtos}>
                    <Text style={styles.titulo_card}>Produtos em Destaque</Text>
                    {carregando ? (
                        <ActivityIndicator color="#fff" style={{ marginTop: 15 }} />
                    ) : produtosDestaque.length === 0 ? (
                        <Text style={styles.texto_vazio}>Nenhum produto cadastrado.</Text>
                    ) : (
                        <View style={styles.ajuste}>
                            {produtosDestaque.map((produto) => (
                                <CardProduto key={produto.id} produto={produto} />
                            ))}
                        </View>
                    )}
                </View>
            </ScrollView>
        </LinearGradient>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    conteudo: {
        padding: 20,
        paddingBottom: 40,
    },
    menu: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop: 10,
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
        marginTop: 20,
        marginBottom: 15,
        flexDirection: 'row',
        alignItems: 'center',
    },
    icone_pessoa: {
        marginRight: 12,
    },
    title: {
        color: '#fff',
        fontSize: 25,
        fontWeight: 'bold',
    },
    subtitulo: {
        fontSize: 20,
        color: '#ccc',
    },
    mensagemErro: {
        color: '#fff',
        textAlign: 'center',
        marginBottom: 10,
        fontSize: 14,
    },

    /* Card principal (grade 2x2) */
    card: {
        backgroundColor: 'rgba(255, 255, 255, 0.28)',
        borderRadius: 15,
        padding: 15,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        gap: 12,
        marginBottom: 15,
    },
    card_menor: {
        backgroundColor: '#ffffff',
        borderRadius: 15,
        padding: 15,
        flexBasis: '47%',
        flexGrow: 1,
    },
    letra: {
        color: '#000000',
        fontSize: 18,
        fontWeight: 'bold',
        paddingBottom: 6,
    },
    fundo: {
        color: '#000000',
        fontSize: 18,
        fontWeight: 'bold',
        backgroundColor: '#0ee83298',
        borderRadius: 5,
        padding: 7,
        alignSelf: 'flex-start',
    },

    /* Alertas */
    card_alerta: {
        backgroundColor: 'rgba(255, 255, 255, 0.28)',
        borderRadius: 15,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
        marginBottom: 15,
    },
    alerta: {
        borderBottomColor: '#fff',
        borderBottomWidth: 2,
        paddingBottom: 8,
        marginBottom: 15,
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    alerta_acao: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    alerta_titulo: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
        padding: 5,
    },
    alerta_espaco: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
    },
    icone_alerta: {
        width: 40,
        textAlign: 'center',
    },
    alerta_textos: {
        flex: 1,
        marginLeft: 12,
    },
    alerta_subtitulo: {
        fontSize: 16,
        color: '#fff',
    },

    /* Produtos em destaque */
    card_produtos: {
        backgroundColor: 'rgba(255, 255, 255, 0.28)',
        borderRadius: 15,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
    },
    titulo_card: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
        paddingBottom: 8,
        marginBottom: 15,
        borderBottomColor: '#fff',
        borderBottomWidth: 2,
    },
    texto_vazio: {
        color: '#fff',
        fontSize: 14,
    },
    ajuste: {
        flexDirection: 'row',
        gap: 10,
    },
    card_produto: {
        flex: 1,
        backgroundColor: '#ffffff',
        borderRadius: 15,
        padding: 10,
        alignItems: 'center',
    },
    imagem_produto: {
        width: 60,
        height: 60,
        borderRadius: 10,
    },
    letra_produtos: {
        color: '#000000',
        fontSize: 15,
        fontWeight: 'bold',
        paddingVertical: 5,
        maxWidth: '100%',
    },
    fundo_produto: {
        color: '#0f5d1c98',
        fontSize: 12,
        fontWeight: 'bold',
        backgroundColor: '#0ab82798',
        borderRadius: 5,
        padding: 2,
    },
});