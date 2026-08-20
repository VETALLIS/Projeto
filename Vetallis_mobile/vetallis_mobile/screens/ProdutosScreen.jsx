
import { LinearGradient } from 'expo-linear-gradient';
import { useState } from 'react';
import { Ionicons, MaterialCommunityIcons, FontAwesome } from '@expo/vector-icons';
import { View, Text, StyleSheet, Image, TouchableOpacity, TextInput } from 'react-native';
export default function DashScreen() {
    const [busca, setBusca] = useState('');
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
                    <View style={styles.iconCircle}>
                        <MaterialCommunityIcons name="cog-outline" size={30} color="#fefefe" />
                    </View>
                </View>
            </View>

            <View style={styles.header}>
                <View>
                    <Text style={styles.title}> Produtos </Text>
                </View>
            </View>
            <View style={styles.searchRow}>
                <View style={styles.searchBar}>
                    <Ionicons name="search" size={18} color="#cbd5e1" style={{ marginRight: 8 }} />
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Buscar produto"
                        placeholderTextColor="#94a3b8"
                        value={busca}
                        onChangeText={setBusca}
                    />
                </View>

                <TouchableOpacity style={styles.filterButton} onPress={() => { /* abrir filtro */ }}>
                    <Ionicons name="filter" size={20} color="#e2e8f0" />
                </TouchableOpacity>
            </View>
            <View style={styles.card}>
                <Image source={require('../assets/vetallis.png')} style={styles.logo_card} />
                <View style={styles.letra}>
                    <View>
                        <View style={styles.ajuste}>
                            <Text style={styles.titulo}>Baytrill</Text>
                            <Text style={styles.fundo}>Vacina</Text>
                        </View>
                        <Text>
                            A vacina é muito top,{"\n"}faz bem pra saúde, apliquem
                        </Text>
                    </View>
                </View>
            </View>
            <View style={styles.card}>
                <Image source={require('../assets/vetallis.png')} style={styles.logo_card} />
                <View style={styles.letra}>
                    <View>
                        <View style={styles.ajuste}>
                            <Text style={styles.titulo}>Baytrill</Text>
                            <Text style={styles.fundo}>Vacina</Text>
                        </View>
                        <Text>
                            A vacina é muito top,{"\n"}faz bem pra saúde, apliquem
                        </Text>
                    </View>
                </View>
            </View>
            <View style={styles.card}>
                <Image source={require('../assets/vetallis.png')} style={styles.logo_card} />
                <View style={styles.letra}>
                    <View>
                        <View style={styles.ajuste}>
                            <Text style={styles.titulo}>Baytrill</Text>
                            <Text style={styles.fundo}>Vacina</Text>
                        </View>
                        <Text>
                            A vacina é muito top,{"\n"}faz bem pra saúde, apliquem
                        </Text>
                    </View>
                </View>
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
        backgroundColor: 'rgba(255, 255, 255, 0.96)',
        borderRadius: 10,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.8,
        shadowRadius: 5,
        elevation: 6,
        maxHeight: 150,
        flexDirection: 'row',
        marginBottom: 20,
        alignSelf: 'center',
        flex: 1,
        justifyContent: 'center',
        gap: 25,
        width: 380


    },
    titulo: {
        alignSelf: 'center',
        fontSize: 18,
        color: '#000000',
        padding: 10
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
    logo_card: {
        width: 120,
        height: 150,
        padding: 10
    },
    header: {
        marginTop: 20,
        marginBottom: 15,
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomColor: '#fff',
        borderBottomWidth: 2,   // <-- adiciona isso
        paddingBottom: 8,
        marginBottom: 20,
        marginTop: 20,
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
        marginTop: 25
    },
    fundo: {
        color: '#4fba24b8',
        fontSize: 12,
        fontWeight: 'bold',
        backgroundColor: '#0ee83298',
        borderRadius: 5,
        marginLeft: 15,
        marginRight: 15,
        alignSelf: 'center',
        padding: 5
    },
    ajuste: {
        flexDirection: 'row'
    },
    searchRow: {
        flexDirection: 'row',
        alignItems: 'center',
        width: '100%',
        marginTop: 16,
        gap: 10,
        marginBottom:50
    },
    searchBar: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(255,255,255,0.08)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.15)',
        borderRadius: 12,
        paddingHorizontal: 14,
        height: 46,
    },
    searchInput: {
        flex: 1,
        color: '#fff',
        fontSize: 15,
    },
    filterButton: {
        width: 46,
        height: 46,
        borderRadius: 12,
        backgroundColor: 'rgba(255,255,255,0.08)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.15)',
        alignItems: 'center',
        justifyContent: 'center',
    },

});