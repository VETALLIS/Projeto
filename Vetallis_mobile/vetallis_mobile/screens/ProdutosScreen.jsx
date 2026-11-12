import { LinearGradient } from 'expo-linear-gradient';
import React, { useState, useMemo, useCallback, useRef } from 'react';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import {
    View, Text, StyleSheet, Image, TouchableOpacity, TextInput,
    FlatList, ActivityIndicator, ScrollView,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useFocusEffect } from '@react-navigation/native';
import { API_URL } from '../src/services/api';
import ModalPedido from '../screens/ModalPedido'; // ajuste o caminho

const LIMITE_ESTOQUE_BAIXO = 5;

// ---------- CARD ----------
const ProdutoCard = React.memo(function ProdutoCard({ item, onEntrada, onSaida }) {
    const qtd = Number(item.quantidade) || 0;
    const zerado = qtd === 0;
    const baixo = qtd > 0 && qtd <= LIMITE_ESTOQUE_BAIXO;
    const corEstoque = zerado ? '#bd0404' : baixo ? '#d9480f' : '#0a7a3d';
    const textoEstoque = zerado ? 'Sem estoque' : `${qtd} em estoque`;

    const uri = item.temImagem
        ? `${API_URL}/api/produtos/${item.id}/imagem${item.atualizadoEm ? `?v=${encodeURIComponent(item.atualizadoEm)}` : ''}`
        : null;

    return (

        <View style={styles.card}>
            <View style={styles.imagemBox}>
                <Image
                    source={uri ? { uri } : require('../assets/vetallis.png')}
                    style={styles.imagem}
                />
                {(zerado || baixo) && (
                    <View style={[styles.selo, { backgroundColor: corEstoque }]}>
                        <Text style={styles.seloTexto}>{zerado ? 'Esgotado' : 'Estoque baixo'}</Text>
                    </View>
                )}
            </View>

            <View style={styles.corpo}>
                <View style={styles.linhaTitulo}>
                    <Text style={styles.nome} numberOfLines={2}>{item.nome}</Text>
                    {!!item.categoria && (
                        <View style={styles.chipCategoria}>
                            <Text style={styles.chipCategoriaTexto}>{item.categoria}</Text>
                        </View>
                    )}
                </View>

                <Text style={styles.descricao} numberOfLines={3}>
                    {item.descricao || 'Sem descrição cadastrada.'}
                </Text>

                <View style={styles.linhaEstoque}>
                    <View style={[styles.pontoEstoque, { backgroundColor: corEstoque }]} />
                    <Text style={[styles.estoque, { color: corEstoque }]}>{textoEstoque}</Text>
                </View>

                <View style={styles.acoes}>
                    <TouchableOpacity
                        style={[styles.botaoAcao, { backgroundColor: '#03A64A' }]}
                        onPress={() => onEntrada(item)}
                        activeOpacity={0.8}
                    >
                        <Ionicons name="arrow-down-circle-outline" size={22} color="#fff" />
                        <Text style={styles.botaoAcaoTexto}>Entrada</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        style={[styles.botaoAcao, { backgroundColor: '#bd0404' }]}
                        onPress={() => onSaida(item)}
                        activeOpacity={0.8}
                    >
                        <Ionicons name="arrow-up-circle-outline" size={22} color="#fff" />
                        <Text style={styles.botaoAcaoTexto}>Saída</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>

    );
});

// ---------- TELA ----------
export default function ProdutosScreen() {
    const insets = useSafeAreaInsets();

    const [busca, setBusca] = useState('');
    const [produtos, setProdutos] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [atualizando, setAtualizando] = useState(false);
    const [erro, setErro] = useState('');
    const jaCarregou = useRef(false);

    // filtros
    const [filtroAberto, setFiltroAberto] = useState(false);
    const [categoriaSel, setCategoriaSel] = useState(null); // null = todas
    const [apenasBaixo, setApenasBaixo] = useState(false);

    // modal de entrada/saída
    const [modal, setModal] = useState({ visivel: false, tipo: 'entrada', produto: null });
    const [referencias, setReferencias] = useState([]);

    const carregarProdutos = useCallback(async ({ manual = false } = {}) => {
        if (manual) setAtualizando(true);
        else if (!jaCarregou.current) setCarregando(true);

        try {
            const resposta = await fetch(`${API_URL}/api/produtos`);
            const dados = await resposta.json();
            if (resposta.ok) {
                setProdutos(dados);
                setErro('');
                jaCarregou.current = true;
            } else if (!jaCarregou.current) {
                setErro(dados.mensagem || 'Não foi possível carregar os produtos.');
            }
        } catch (e) {
            if (!jaCarregou.current) setErro('Não foi possível conectar ao servidor.');
        } finally {
            setCarregando(false);
            setAtualizando(false);
        }
    }, []);

    // recarrega ao focar a aba + a cada 10s enquanto ela estiver aberta
    useFocusEffect(
        useCallback(() => {
            carregarProdutos();
            const id = setInterval(() => carregarProdutos(), 10000);
            return () => clearInterval(id);
        }, [carregarProdutos])
    );

    // categorias vindas dos próprios produtos
    const categorias = useMemo(() => {
        const set = new Set(produtos.map((p) => p.categoria).filter(Boolean));
        return Array.from(set).sort((a, b) => a.localeCompare(b));
    }, [produtos]);

    const qtdFiltrosAtivos = (categoriaSel ? 1 : 0) + (apenasBaixo ? 1 : 0);

    const produtosFiltrados = useMemo(() => {
        const termo = busca.trim().toLowerCase();
        return produtos.filter((p) => {
            if (categoriaSel && p.categoria !== categoriaSel) return false;
            if (apenasBaixo && !(Number(p.quantidade) <= LIMITE_ESTOQUE_BAIXO)) return false;
            if (!termo) return true;
            return (
                p.nome?.toLowerCase().includes(termo) ||
                p.categoria?.toLowerCase().includes(termo) ||
                p.descricao?.toLowerCase().includes(termo)
            );
        });
    }, [busca, produtos, categoriaSel, apenasBaixo]);

    function limparFiltros() {
        setCategoriaSel(null);
        setApenasBaixo(false);
    }

    // ---------- MODAL ----------
    // O modal espera "estoque_quantidade"; aqui o campo se chama "quantidade"
    const produtosParaModal = useMemo(
        () => produtos.map((p) => ({ ...p, estoque_quantidade: p.quantidade })),
        [produtos]
    );

    async function abrirModal(tipo, produto) {
        setReferencias([]);
        setModal({
            visivel: true,
            tipo,
            produto: { ...produto, estoque_quantidade: produto.quantidade },
        });

        // AJUSTE os endpoints para os do seu backend
        const rota = tipo === 'entrada' ? 'fornecedores' : 'animais';
        try {
            const r = await fetch(`${API_URL}/api/${rota}`);
            const d = await r.json();
            if (r.ok) setReferencias(d.map((x) => ({ id: x.id, nome: x.nome, subtitulo: x.subtitulo })));
        } catch (e) {
            // a lista fica vazia e o modal mostra "Nenhum ... disponível"
        }
    }

    function fecharModal() {
        setModal((m) => ({ ...m, visivel: false }));
    }

    async function confirmarPedido(pedido) {
        // AJUSTE a rota e, se precisar, o header de autenticação
        const r = await fetch(`${API_URL}/api/pedidos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pedido),
        });
        const d = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(d.mensagem || 'Erro ao enviar pedido');
        carregarProdutos(); // estoque atualizado na hora
    }

    const renderProduto = useCallback(
        ({ item }) => (
            <ProdutoCard
                item={item}
                onEntrada={(p) => abrirModal('entrada', p)}
                onSaida={(p) => abrirModal('saida', p)}
            />
        ),
        []
    );

    // ---------- RENDER ----------
    return (
        <LinearGradient
            colors={['#000000', '#0d3b2e', '#0a4a3a', '#1a6b4a']}
            locations={[0, 0.3, 0.6, 1]}
            start={{ x: 0.2, y: 0.1 }}
            end={{ x: 1, y: 1 }}
            style={[styles.container, { paddingTop: insets.top + 10 }]}
        >
            <View style={styles.menu}>
                <Image source={require('../assets/vetallis.png')} style={styles.logo} />
            </View>

            <View style={styles.header}>
                <Text style={styles.title}>Produtos</Text>
                <Text style={styles.contador}>
                    {produtosFiltrados.length} {produtosFiltrados.length === 1 ? 'item' : 'itens'}
                </Text>
            </View>

            <View style={styles.searchRow}>
                <View style={styles.searchBar}>
                    <Ionicons name="search" size={20} color="#cbd5e1" style={{ marginRight: 10 }} />
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Buscar produto"
                        placeholderTextColor="#94a3b8"
                        value={busca}
                        onChangeText={setBusca}
                        returnKeyType="search"
                    />
                    {!!busca && (
                        <TouchableOpacity onPress={() => setBusca('')} hitSlop={10}>
                            <Ionicons name="close-circle" size={20} color="#94a3b8" />
                        </TouchableOpacity>
                    )}
                </View>

                <TouchableOpacity
                    style={[styles.filterButton, (filtroAberto || qtdFiltrosAtivos > 0) && styles.filterButtonAtivo]}
                    onPress={() => setFiltroAberto((v) => !v)}
                >
                    <Ionicons name="options-outline" size={24} color="#e2e8f0" />
                    {qtdFiltrosAtivos > 0 && (
                        <View style={styles.filterBadge}>
                            <Text style={styles.filterBadgeTexto}>{qtdFiltrosAtivos}</Text>
                        </View>
                    )}
                </TouchableOpacity>
            </View>

            {filtroAberto && (
                <View style={styles.painelFiltro}>
                    <TouchableOpacity
                        style={styles.linhaSwitch}
                        onPress={() => setApenasBaixo((v) => !v)}
                        activeOpacity={0.7}
                    >
                        <Ionicons
                            name={apenasBaixo ? 'checkbox' : 'square-outline'}
                            size={24}
                            color={apenasBaixo ? '#4ade80' : '#cbd5e1'}
                        />
                        <Text style={styles.textoSwitch}>
                            Só estoque baixo (até {LIMITE_ESTOQUE_BAIXO})
                        </Text>
                    </TouchableOpacity>

                    {categorias.length > 0 && (
                        <>
                            <Text style={styles.rotuloFiltro}>Categoria</Text>
                            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8 }}>
                                {[null, ...categorias].map((cat) => {
                                    const ativo = categoriaSel === cat;
                                    return (
                                        <TouchableOpacity
                                            key={cat ?? 'todas'}
                                            style={[styles.chipFiltro, ativo && styles.chipFiltroAtivo]}
                                            onPress={() => setCategoriaSel(cat)}
                                        >
                                            <Text style={[styles.chipFiltroTexto, ativo && styles.chipFiltroTextoAtivo]}>
                                                {cat ?? 'Todas'}
                                            </Text>
                                        </TouchableOpacity>
                                    );
                                })}
                            </ScrollView>
                        </>
                    )}

                    {qtdFiltrosAtivos > 0 && (
                        <TouchableOpacity onPress={limparFiltros} style={styles.limparFiltros}>
                            <Text style={styles.limparFiltrosTexto}>Limpar filtros</Text>
                        </TouchableOpacity>
                    )}
                </View>
            )}

            {carregando ? (
                <ActivityIndicator size="large" color="#fff" style={{ marginTop: 30 }} />
            ) : erro ? (
                <View style={styles.vazio}>
                    <Text style={styles.mensagemErro}>{erro}</Text>
                    <TouchableOpacity style={styles.botaoTentar} onPress={() => carregarProdutos()}>
                        <Text style={styles.botaoTentarTexto}>Tentar de novo</Text>
                    </TouchableOpacity>
                </View>
            ) : (
                <FlatList
                    data={produtosFiltrados}
                    keyExtractor={(item) => String(item.id)}
                    renderItem={renderProduto}
                    showsVerticalScrollIndicator={false}
                    onRefresh={() => carregarProdutos({ manual: true })}
                    refreshing={atualizando}
                    keyboardShouldPersistTaps="handled"
                    contentContainerStyle={{ paddingBottom: insets.bottom + 24 }}
                    ListEmptyComponent={
                        <Text style={styles.mensagemErro}>Nenhum produto encontrado.</Text>
                    }
                />
            )}

            <ModalPedido
                visible={modal.visivel}
                tipo={modal.tipo}
                produtoInicial={modal.produto}
                produtosDisponiveis={produtosParaModal}
                referenciasDisponiveis={referencias}
                onClose={fecharModal}
                onConfirmar={confirmarPedido}
            />
        </LinearGradient>
    );
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 18,
    },
    menu: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    logo: { width: 56, height: 56 },
    iconCircle: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: 'rgba(255,255,255,0.15)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    header: {
        marginTop: 14,
        marginBottom: 16,
        flexDirection: 'row',
        alignItems: 'baseline',
        justifyContent: 'space-between',
        borderBottomColor: '#fff',
        borderBottomWidth: 2,
        paddingBottom: 8,
    },
    title: { color: '#fff', fontSize: 30, fontWeight: 'bold' },
    contador: { color: '#cbd5e1', fontSize: 15 },

    // busca / filtro
    searchRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 10,
        marginBottom: 14,
    },
    searchBar: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(255,255,255,0.10)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.18)',
        borderRadius: 14,
        paddingHorizontal: 14,
        height: 52,
    },
    searchInput: { flex: 1, color: '#fff', fontSize: 17 },
    filterButton: {
        width: 52,
        height: 52,
        borderRadius: 14,
        backgroundColor: 'rgba(255,255,255,0.10)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.18)',
        alignItems: 'center',
        justifyContent: 'center',
    },
    filterButtonAtivo: {
        backgroundColor: 'rgba(74,222,128,0.22)',
        borderColor: '#4ade80',
    },
    filterBadge: {
        position: 'absolute',
        top: -6,
        right: -6,
        minWidth: 20,
        height: 20,
        borderRadius: 10,
        backgroundColor: '#4ade80',
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: 4,
    },
    filterBadgeTexto: { color: '#052e16', fontSize: 12, fontWeight: 'bold' },
    painelFiltro: {
        backgroundColor: 'rgba(0,0,0,0.30)',
        borderRadius: 14,
        padding: 14,
        marginBottom: 14,
    },
    linhaSwitch: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 6 },
    textoSwitch: { color: '#fff', fontSize: 16 },
    rotuloFiltro: { color: '#cbd5e1', fontSize: 14, marginTop: 12, marginBottom: 8 },
    chipFiltro: {
        paddingHorizontal: 16,
        paddingVertical: 9,
        borderRadius: 20,
        backgroundColor: 'rgba(255,255,255,0.10)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.2)',
    },
    chipFiltroAtivo: { backgroundColor: '#4ade80', borderColor: '#4ade80' },
    chipFiltroTexto: { color: '#e2e8f0', fontSize: 15 },
    chipFiltroTextoAtivo: { color: '#052e16', fontWeight: 'bold' },
    limparFiltros: { alignSelf: 'flex-end', marginTop: 12, paddingVertical: 4 },
    limparFiltrosTexto: { color: '#4ade80', fontSize: 15, fontWeight: '600' },

    // card
    card: {
        backgroundColor: '#fff',
        borderRadius: 18,
        marginBottom: 20,
        overflow: 'hidden',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.35,
        shadowRadius: 8,
        elevation: 6,
        width: '88%',
        maxWidth: 400,
        alignSelf: 'center',
    },
    imagemBox: {
        height: 150,
        backgroundColor: '#eef3ef',
        alignItems: 'center',
        justifyContent: 'center',
    },
    imagem: { width: '100%', height: '100%', resizeMode: 'contain' },
    selo: {
        position: 'absolute',
        top: 12,
        left: 12,
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 8,
    },
    seloTexto: { color: '#fff', fontSize: 13, fontWeight: 'bold' },
    corpo: { padding: 16 },
    linhaTitulo: {
        flexDirection: 'row',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        gap: 10,
    },
    nome: { flex: 1, fontSize: 21, fontWeight: 'bold', color: '#111' },
    chipCategoria: {
        backgroundColor: '#d6f5df',
        borderRadius: 8,
        paddingHorizontal: 10,
        paddingVertical: 5,
        marginTop: 2,
    },
    chipCategoriaTexto: { color: '#0a5c2e', fontSize: 13, fontWeight: 'bold' },
    descricao: { color: '#444', fontSize: 15, lineHeight: 21, marginTop: 8 },
    linhaEstoque: { flexDirection: 'row', alignItems: 'center', marginTop: 12, gap: 8 },
    pontoEstoque: { width: 10, height: 10, borderRadius: 5 },
    estoque: { fontSize: 16, fontWeight: 'bold' },
    acoes: { flexDirection: 'row', gap: 12, marginTop: 16 },
    botaoAcao: {
        flex: 1,
        height: 50,
        borderRadius: 12,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 8,
    },
    botaoAcaoTexto: { color: '#fff', fontSize: 17, fontWeight: 'bold' },

    // estados
    vazio: { alignItems: 'center' },
    mensagemErro: { color: '#fff', textAlign: 'center', marginTop: 30, fontSize: 16 },
    botaoTentar: {
        marginTop: 16,
        paddingHorizontal: 20,
        paddingVertical: 12,
        borderRadius: 12,
        backgroundColor: 'rgba(255,255,255,0.15)',
    },
    botaoTentarTexto: { color: '#fff', fontSize: 16, fontWeight: '600' },
});