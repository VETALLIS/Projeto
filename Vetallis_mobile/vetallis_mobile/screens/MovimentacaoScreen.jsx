import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useState, useEffect, useMemo } from 'react';
import { API_URL } from '../src/services/api';

import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, ActivityIndicator, TextInput } from 'react-native';

// "2026-11-19" ou "2026-11-19T03:00:00.000Z" -> "19/11/2026"
function formatarData(data) {
  if (!data) return '';
  const m = String(data).match(/^(\d{4})-(\d{2})-(\d{2})/);
  return m ? `${m[3]}/${m[2]}/${m[1]}` : String(data);
}

const FILTROS = [
  { valor: 'Todos', rotulo: 'Todos' },
  { valor: 'Entrada', rotulo: 'Entradas' },
  { valor: 'Saída', rotulo: 'Saídas' },
];

export default function MovimentacaoScreen() {
  const [search, setSearch] = useState('');
  const [filtro, setFiltro] = useState('Todos');
  const [historico, setHistorico] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  async function carregarHistorico() {
    setCarregando(true);
    setErro('');
    try {
      const resposta = await fetch(`${API_URL}/api/historico`);
      const dados = await resposta.json();
      if (resposta.ok) {
        setHistorico(dados);
      } else {
        setErro(dados.mensagem || 'Não foi possível carregar o histórico.');
      }
    } catch (e) {
      setErro('Não foi possível conectar ao servidor.');
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregarHistorico();
  }, []);

  // Aplica o filtro (Todos/Entradas/Saídas) e a busca por nome do produto
  const filteredHistory = useMemo(() => {
    const termo = search.trim().toLowerCase();
    return historico.filter((item) => {
      const tipoOk = filtro === 'Todos' || item.tipo === filtro;
      const buscaOk = !termo || item.produto?.toLowerCase().includes(termo);
      return tipoOk && buscaOk;
    });
  }, [search, filtro, historico]);

  // Soma a QUANTIDADE de itens (não a contagem de pedidos) de cada tipo
  const { totalEntradas, totalSaidas } = useMemo(() => {
    return historico.reduce(
      (totais, item) => {
        const qtd = Number(item.quantidade) || 0;
        if (item.tipo === 'Entrada') {
          totais.totalEntradas += qtd;
        } else if (item.tipo === 'Saída') {
          totais.totalSaidas += qtd;
        }
        return totais;
      },
      { totalEntradas: 0, totalSaidas: 0 }
    );
  }, [historico]);

  // Parte de cima da lista (resumo, busca e filtros). Rola junto com os cards.
  const topoDaLista = (
    <View>
      <View style={styles.statsContainer}>
        <View style={[styles.statsCard, { backgroundColor: 'rgba(34, 197, 94, 0.18)' }]}>
          <View style={styles.statsTopo}>
            <Ionicons name="arrow-down-circle" size={22} color="#22C55E" />
            <Text style={styles.statsLabel}>Entradas</Text>
          </View>
          <Text style={styles.statsNumber}>{totalEntradas}</Text>
        </View>

        <View style={[styles.statsCard, { backgroundColor: 'rgba(239, 68, 68, 0.18)' }]}>
          <View style={styles.statsTopo}>
            <Ionicons name="arrow-up-circle" size={22} color="#EF4444" />
            <Text style={styles.statsLabel}>Saídas</Text>
          </View>
          <Text style={styles.statsNumber}>{totalSaidas}</Text>
        </View>
      </View>

      <View style={styles.searchBox}>
        <Ionicons name="search" size={20} color="#ffffffaa" />
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar produto"
          placeholderTextColor="#ffffff88"
          value={search}
          onChangeText={setSearch}
        />
        {search !== '' && (
          <TouchableOpacity onPress={() => setSearch('')}>
            <Ionicons name="close-circle" size={20} color="#ffffffaa" />
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.filtros}>
        {FILTROS.map((f) => {
          const ativo = filtro === f.valor;
          return (
            <TouchableOpacity
              key={f.valor}
              style={[styles.chip, ativo && styles.chipAtivo]}
              onPress={() => setFiltro(f.valor)}
            >
              <Text style={[styles.chipTexto, ativo && styles.chipTextoAtivo]}>{f.rotulo}</Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );

  return (
    <LinearGradient
      colors={['#000000', '#0d3b2e', '#0a4a3a', '#1a6b4a']}
      locations={[0, 0.3, 0.6, 1]}
      start={{ x: 0.2, y: 0.1 }}
      end={{ x: 1, y: 1 }}
      style={styles.container}
    >
      {/* LOGO */}
      <View style={styles.menu}>
        <Image source={require('../assets/vetallis.png')} style={styles.logo} />
      </View>

      {/* TÍTULO */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>Histórico</Text>
          <Text style={styles.subtitle}>Movimentações do estoque</Text>
        </View>

        <TouchableOpacity style={styles.filterButton} onPress={carregarHistorico}>
          <Ionicons name="refresh" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* LISTA */}
      <FlatList
        data={filteredHistory}
        keyExtractor={(item, index) => `${item.tipo}-${item.id}-${index}`}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 40 }}
        keyboardShouldPersistTaps="handled"
        ListHeaderComponent={topoDaLista}
        onRefresh={carregarHistorico}
        refreshing={carregando && historico.length > 0}
        ListEmptyComponent={
          carregando ? (
            <ActivityIndicator size="large" color="#fff" style={{ marginTop: 30 }} />
          ) : (
            <Text style={styles.mensagemErro}>
              {erro || 'Nenhuma movimentação encontrada.'}
            </Text>
          )
        }
        renderItem={({ item }) => {
          const entrada = item.tipo === 'Entrada';
          const cor = entrada ? '#22C55E' : '#EF4444';

          return (
            <View style={[styles.card, { borderLeftColor: cor }]}>
              <View style={[styles.iconContainer, { backgroundColor: entrada ? 'rgba(34, 197, 94, 0.18)' : 'rgba(239, 68, 68, 0.18)' }]}>
                <Ionicons
                  name={entrada ? 'arrow-down-circle' : 'arrow-up-circle'}
                  size={28}
                  color={cor}
                />
              </View>

              <View style={styles.info}>
                <Text style={styles.product} numberOfLines={1}>{item.produto}</Text>

                <View style={styles.detailsRow}>
                  <Text style={[styles.type, { color: cor }]}>{item.tipo}</Text>
                  <Text style={styles.separadorPonto}>•</Text>
                  <Ionicons name="calendar-outline" size={13} color="#CBD5E1" />
                  <Text style={styles.date}>{formatarData(item.data)}</Text>
                </View>
              </View>

              <View style={styles.quantidadeBox}>
                <Text style={[styles.quantidade, { color: cor }]}>
                  {entrada ? '+' : '-'}{item.quantidade}
                </Text>
                <Text style={styles.quantidadeLabel}>un.</Text>
              </View>
            </View>
          );
        }}
      />
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
  },

  menu: {
    marginTop: 10,
    flexDirection: 'row',
    alignItems: 'center',
  },
  logo: {
    width: 60,
    height: 60,
  },

  header: {
    marginTop: 20,
    marginBottom: 20,
    paddingBottom: 12,
    borderBottomColor: '#fff',
    borderBottomWidth: 2,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
  },
  subtitle: {
    color: '#ffffffcc',
    marginTop: 2,
    fontSize: 15,
  },
  filterButton: {
    width: 48,
    height: 48,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Resumo
  statsContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  statsCard: {
    flex: 1,
    borderRadius: 20,
    padding: 16,
  },
  statsTopo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  statsNumber: {
    color: '#fff',
    fontSize: 30,
    fontWeight: 'bold',
    marginTop: 8,
  },
  statsLabel: {
    color: '#E2E8F0',
    fontSize: 14,
    fontWeight: '600',
  },

  // Busca e filtros
  searchBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 14,
    paddingHorizontal: 14,
    marginBottom: 12,
    gap: 8,
  },
  searchInput: {
    flex: 1,
    color: '#fff',
    fontSize: 15,
    paddingVertical: 12,
  },
  filtros: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 18,
  },
  chip: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.12)',
  },
  chipAtivo: {
    backgroundColor: '#03A64A',
  },
  chipTexto: {
    color: '#E2E8F0',
    fontWeight: '600',
    fontSize: 14,
  },
  chipTextoAtivo: {
    color: '#fff',
  },

  // Cards da lista
  card: {
    backgroundColor: 'rgba(255, 255, 255, 0.12)',
    borderRadius: 18,
    borderLeftWidth: 4,
    padding: 14,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconContainer: {
    width: 52,
    height: 52,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  info: {
    flex: 1,
  },
  product: {
    color: '#fff',
    fontSize: 17,
    fontWeight: 'bold',
  },
  detailsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 6,
    gap: 5,
  },
  type: {
    fontSize: 13,
    fontWeight: 'bold',
  },
  separadorPonto: {
    color: '#CBD5E1',
    fontSize: 13,
  },
  date: {
    color: '#CBD5E1',
    fontSize: 13,
  },
  quantidadeBox: {
    alignItems: 'flex-end',
    marginLeft: 10,
  },
  quantidade: {
    fontSize: 22,
    fontWeight: 'bold',
  },
  quantidadeLabel: {
    color: '#CBD5E1',
    fontSize: 12,
  },

  mensagemErro: {
    color: '#fff',
    textAlign: 'center',
    marginTop: 30,
    fontSize: 15,
  },
});