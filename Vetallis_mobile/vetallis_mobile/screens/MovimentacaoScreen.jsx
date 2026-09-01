import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useState, useEffect, useMemo } from 'react'

import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';

// Mesmo IP/porta usados nas outras telas — se você já centralizou isso em
// src/services/api.js, troque essa constante por um import de lá.
const API_URL = 'http://10.135.60.38:3000';

export default function MovimentacaoScreen() {
  const [search, setSearch] = useState('');
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

  const filteredHistory = useMemo(() => {
    const termo = search.toLowerCase();
    return historico.filter(
      (item) =>
        item.produto?.toLowerCase().includes(termo) ||
        item.tipo?.toLowerCase().includes(termo)
    );
  }, [search, historico]);

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

  return (
    <LinearGradient
      colors={['#000000', '#0d3b2e', '#0a4a3a', '#1a6b4a']}
      locations={[0, 0.3, 0.6, 1]}
      start={{ x: 0.2, y: 0.1 }}
      end={{ x: 1, y: 1 }}
      style={styles.container}
    >
      <View style={styles.container}>
        {/* HEADER */}
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
            <View style={styles.iconCircle}>
              <MaterialCommunityIcons name="cog-outline" size={30} color="#fefefe" />
            </View>
          </View>
        </View>

        <View style={styles.header}>
          <View>
            <Text style={styles.title}>
              Histórico
            </Text>

            <Text style={styles.subtitle}>
              Movimentações do estoque
            </Text>
          </View>

          <TouchableOpacity style={styles.filterButton} onPress={carregarHistorico}>
            <Ionicons
              name="refresh"
              size={24}
              color="#fff"
            />
          </TouchableOpacity>
        </View>

        {/* ESTATÍSTICAS */}

        <View style={styles.statsContainer}>
          <View style={styles.statsCardGreen}>
            <Ionicons
              name="arrow-down-circle"
              size={24}
              color="#22C55E"
            />

            <Text style={styles.statsNumber}>
              {totalEntradas}
            </Text>

            <Text style={styles.statsLabel}>
              Entradas
            </Text>
          </View>

          <View style={styles.statsCardRed}>
            <Ionicons
              name="arrow-up-circle"
              size={24}
              color="#EF4444"
            />

            <Text style={styles.statsNumber}>
              {totalSaidas}
            </Text>

            <Text style={styles.statsLabel}>
              Saídas
            </Text>
          </View>
        </View>

        {/* LISTA */}

        {carregando ? (
          <ActivityIndicator size="large" color="#fff" style={{ marginTop: 30 }} />
        ) : erro ? (
          <Text style={styles.mensagemErro}>{erro}</Text>
        ) : (
          <FlatList
            data={filteredHistory}
            keyExtractor={(item, index) => `${item.tipo}-${item.id}-${index}`}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={{
              paddingBottom: 40,
            }}
            onRefresh={carregarHistorico}
            refreshing={carregando}
            ListEmptyComponent={
              <Text style={styles.mensagemErro}>Nenhuma movimentação encontrada.</Text>
            }
            renderItem={({ item }) => (
              <View style={styles.card}>
                {/* ÍCONE */}

                <View
                  style={[
                    styles.iconContainer,
                    {
                      backgroundColor:
                        item.tipo === 'Entrada'
                          ? '#007204'
                          : '#450A0A',
                    },
                  ]}
                >
                  <Ionicons
                    name={
                      item.tipo === 'Entrada'
                        ? 'arrow-down-circle'
                        : 'arrow-up-circle'
                    }
                    size={30}
                    color={
                      item.tipo === 'Entrada'
                        ? '#22C55E'
                        : '#EF4444'
                    }
                  />
                </View>

                {/* INFO */}

                <View style={styles.info}>
                  <View style={styles.topRow}>
                    <Text style={styles.product}>
                      {item.produto}
                    </Text>

                    <Text
                      style={[
                        styles.type,
                        {
                          color:
                            item.tipo === 'Entrada'
                              ? '#86EFAC'
                              : '#FCA5A5',
                        },
                      ]}
                    >
                      {item.tipo}
                    </Text>
                  </View>

                  <View style={styles.detailsRow}>
                    <Text style={styles.quantity}>
                      Quantidade: {item.quantidade}
                    </Text>

                    <Text style={styles.date}>
                      {item.data}
                    </Text>
                  </View>
                </View>
              </View>
            )}
          />
        )}
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
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

  subtitle: {
    color: '#ffffff',
    marginTop: 5,
    fontSize: 15,
  },

  filterButton: {
    width: 52,
    height: 52,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },

  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 25,
  },

  statsCardGreen: {
    width: '48%',
    backgroundColor: '#024b20',
    borderRadius: 24,
    padding: 20,
  },

  statsCardRed: {
    width: '48%',
    backgroundColor: '#450A0A',
    borderRadius: 24,
    padding: 20,
  },

  statsNumber: {
    color: '#fff',
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 12,
  },

  statsLabel: {
    color: '#CBD5E1',
    marginTop: 6,
  },

  card: {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 24,
    padding: 18,
    marginBottom: 18,
    flexDirection: 'row',
  },

  iconContainer: {
    width: 65,
    height: 65,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },

  info: {
    flex: 1,
  },

  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  product: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    flex: 1,
    marginRight: 10,
  },

  type: {
    fontSize: 14,
    fontWeight: 'bold',
  },

  detailsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },

  quantity: {
    color: '#CBD5E1',
    fontSize: 14,
  },

  date: {
    color: '#ffffff',
    fontSize: 13,
  },

  hour: {
    color: '#ffffff',
    marginTop: 8,
    fontSize: 13,
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
  mensagemErro: {
    color: '#fff',
    textAlign: 'center',
    marginTop: 30,
    fontSize: 15,
  },
});