
import { View, Text, StyleSheet } from 'react-native';
export default function DashScreen() {
    return (
            <View style={styles.overlay}>
                <Text style={styles.title}>Bem Vindo a Vetallis!</Text>
                <Text style={styles.subtitle}>Gerenciamento de Estoque de medicamentos!!! </Text>
            </View>
    )
}

const styles = StyleSheet.create({
    background: {
        flex: 1,
        resizeMode: 'cover',
        justifyContent: 'center',
    },
    overlay: {
        backgroundColor: 'rgba(0,0,0,0.6)',
        padding: 20,
        borderRadius: 10,
        alignItems: 'center',
        margin: 20
    },
    title: {
        color: ' #fff',
        fontSize: 28,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    subtitle: {
        color: '#fff',
        fontSize: 16,
    }
})