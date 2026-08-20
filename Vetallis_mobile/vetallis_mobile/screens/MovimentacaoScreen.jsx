
import { LinearGradient, search } from 'expo-linear-gradient';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useState } from 'react'

import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
} from 'react-native';


export default function MovimentacaoScreen() {
   const [search, setSearch] = useState('');
  const history = [
    {
      id: 1,
      type: 'Entrada',
      product: 'Dipirona',
      quantity: 50,
      date: '20/05/2026',
      hour: '09:30',
    },

    {
      id: 2,
      type: 'Saída',
      product: 'Vermífugo',
      quantity: 15,
      date: '18/05/2026',
      hour: '10:15',
    },

    {
      id: 3,
      type: 'Entrada',
      product: 'Vacinas',
      quantity: 150,
      date: '15/05/2026',
      hour: '11:40',
    },

    {
      id: 4,
      type: 'Saída',
      product: 'Losartana',
      quantity: 5,
      date: '10/05/2026',
      hour: '13:20',
    },

    {
      id: 5,
      type: 'Entrada',
      product: 'Loratadina',
      quantity: 50,
      date: '09/05/2026',
      hour: '08:50',
    },
  ];

  const filteredHistory = history.filter(
    (item) =>
      item.product
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      item.type
        .toLowerCase()
        .includes(search.toLowerCase())
  );

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

          <TouchableOpacity style={styles.filterButton}>
            <Ionicons
              name="calendar-outline"
              size={24}
              color="#fff"
            />
          </TouchableOpacity>
        </View>

        {/* PESQUISA */}

        {/* ESTATÍSTICAS */}

        <View style={styles.statsContainer}>
          <View style={styles.statsCardGreen}>
            <Ionicons
              name="arrow-down-circle"
              size={24}
              color="#22C55E"
            />

            <Text style={styles.statsNumber}>
              18
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
              9
            </Text>

            <Text style={styles.statsLabel}>
              Saídas
            </Text>
          </View>
        </View>

        {/* LISTA */}

        <FlatList
          data={filteredHistory}
          keyExtractor={(item) =>
            item.id.toString()
          }
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{
            paddingBottom: 40,
          }}
          renderItem={({ item }) => (
            <View style={styles.card}>
              {/* ÍCONE */}

              <View
                style={[
                  styles.iconContainer,
                  {
                    backgroundColor:
                      item.type === 'Entrada'
                        ? '#007204'
                        : '#450A0A',
                  },
                ]}
              >
                <Ionicons
                  name={
                    item.type === 'Entrada'
                      ? 'arrow-down-circle'
                      : 'arrow-up-circle'
                  }
                  size={30}
                  color={
                    item.type === 'Entrada'
                      ? '#22C55E'
                      : '#EF4444'
                  }
                />
              </View>

              {/* INFO */}

              <View style={styles.info}>
                <View style={styles.topRow}>
                  <Text style={styles.product}>
                    {item.product}
                  </Text>

                  <Text
                    style={[
                      styles.type,
                      {
                        color:
                          item.type === 'Entrada'
                            ? '#86EFAC'
                            : '#FCA5A5',
                      },
                    ]}
                  >
                    {item.type}
                  </Text>
                </View>

                <View style={styles.detailsRow}>
                  <Text style={styles.quantity}>
                    Quantidade: {item.quantity}
                  </Text>

                  <Text style={styles.date}>
                    {item.date}
                  </Text>
                </View>

                <Text style={styles.hour}>
                  {item.hour}
                </Text>
              </View>
            </View>
          )}
        />
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
    backgroundColor: 'rgba(255, 255, 255, 0.15);',
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
    backgroundColor: 'rgba(255, 255, 255, 0.15);',
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
});