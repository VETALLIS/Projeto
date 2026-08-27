import AsyncStorage from '@react-native-async-storage/async-storage';

export async function logOut(navigation) {
  try {
    // Remove todos os dados de uma vez
    await AsyncStorage.multiRemove(['userToken', 'userData', 'refreshToken']);
    
    // Redireciona usando o NOME da rota cadastrada no seu Navigator (em formato de String)
    navigation.replace('Login'); 
  } catch (error) {
    console.warn('Erro ao fazer logout:', error);
  }
}
