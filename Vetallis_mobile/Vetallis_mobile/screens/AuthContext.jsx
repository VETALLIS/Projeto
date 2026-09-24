import { createContext, useContext, useState } from 'react';
import { registrarPushToken } from '../utilidade/notification'

// Guarda o usuário logado (id, nome, email, cargo) e disponibiliza
// para qualquer tela do app através do hook useAuth().
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);

  useEffect(() => {
    if (usuario?.id) {
      registrarPushToken(usuario.id);
    }
  }, [usuario]);

  return (
    <AuthContext.Provider value={{ usuario, setUsuario }}>
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