
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';

export default function ProdutosScreen({ route, navigation }) {

    return (
        <View style={styles.container}>
            <Text style={styles.nome}>Produtos presentes no estoque</Text>
        </View>

    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: '#0f172a',
        alignItems: 'center',
    },
    image: {
        width: '100%',
        height: 250,
        borderRadius: 12,
        marginBottom: 20,
    },
    nome: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fff',
    },
    preco: {
        fontSize: 20,
        color: '#4cd964',
        marginVertical: 10,
    },
    desc: {
        color: '#ccc',
        textAlign: 'center',
        marginBottom: 20,
    },
    botao: {
        backgroundColor: '#3b82f6',
        padding: 15,
        borderRadius: 10,
        width: '100%',
        alignItems: 'center',
    },
    botaoTexto: {
        color: '#fff',
        fontWeight: 'bold',
    },
    voltar: {
        color: '#aaa',
        marginTop: 15,
    },
});
