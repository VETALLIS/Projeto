import { createContext, useContext, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
// import { registrarPushToken } from '../utilidade/notification';

// Guarda o usuário logado (id, nome, email, cargo) e disponibiliza
// para qualquer tela do app através do hook useAuth().
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);

  /*
  useEffect(() => {
    if (usuario?.id) {
      registrarPushToken(usuario.id);
    }
  }, [usuario]);
  */

  // Limpa a sessão. Não apaga 'lembrar', 'emailSalvo' nem 'senhaSalva',
  // para o "Lembrar-me" continuar funcionando na tela de login.
  async function sair() {
    try {
      await AsyncStorage.multiRemove(['userToken', 'userData', 'refreshToken']);
    } catch (error) {
      console.warn('Erro ao limpar dados no logout:', error);
    } finally {
      setUsuario(null);
    }
  }

  return (
    <AuthContext.Provider value={{ usuario, setUsuario, sair }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const contexto = useContext(AuthContext);
  if (!contexto) {
    throw new Error('useAuth precisa ser usado dentro de um <AuthProvider>');
  }
  return contexto;
}