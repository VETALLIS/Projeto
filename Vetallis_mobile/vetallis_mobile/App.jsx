import { NavigationContainer, DarkTheme } from '@react-navigation/native';
import { View, Alert } from 'react-native'; 
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { logOut } from './screens/LogOut'; 
import DashScreen from './screens/DashboardScreen';
import PerfilScreen from './screens/GerenciarPerfilScreen';
import LeitorScreen from './screens/LeitorQRCodeScreen';
import MovimentacaoScreen from './screens/MovimentacaoScreen';
import ProdutosScreen from './screens/ProdutosScreen';
import LoginScreen from './screens/LoginScrenn';
import { AuthProvider } from './screens/AuthContext';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#4cd964',
        tabBarInactiveTintColor: '#888',
      }}
    >
      <Tab.Screen
        name="Home"
        component={DashScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home-outline" size={size} color={color} />
          ),
        }}
      />

      <Tab.Screen
        name="Produtos"
        component={ProdutosScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="pill" size={size} color={color} />
          ),
        }}
      />


      <Tab.Screen
        name="Histórico"
        component={MovimentacaoScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="bar-chart-outline" size={size} color={color} />
          ),
        }}
      />

      <Tab.Screen
        name="Movimentação"
        component={LeitorScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="cube-outline" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Perfil"
        component={PerfilScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person-outline" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Logout"
        component={View} // Coloque um componente vazio qualquer (não será renderizado)
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="arrow-right-circle-outline" size={size} color={color} />
          ),
        }}
        listeners={({ navigation }) => ({
          tabPress: (e) => {
            // 1. Impede a navegação padrão (não abre uma tela de logout)
            e.preventDefault();

            // 2. Pergunta ao usuário se ele realmente quer sair
            Alert.alert('Sair', 'Deseja realmente sair da conta?', [
              { text: 'Cancelar', style: 'cancel' },
              {
                text: 'Sair',
                style: 'destructive',
                onPress: () => logOut(navigation) // Executa a sua função de logout
              },
            ]);
          },
        })}
      />
    </Tab.Navigator>

  );
}
export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer theme={DarkTheme}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="App" component={TabNavigator} />
        </Stack.Navigator>
      </NavigationContainer>
    </AuthProvider>
  );
}