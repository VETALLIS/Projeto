import axios from 'axios';
import Constants from 'expo-constants';

function obterIpDoComputador() {
  const hostUri =
    Constants.expoConfig?.hostUri ||
    Constants.manifest2?.extra?.expoGo?.debuggerHost ||
    Constants.manifest?.debuggerHost;

  if (hostUri) {
    return hostUri.split(':')[0]; // pega só o IP, sem a porta do Metro
  }

  // Fallback caso não consiga detectar (ex: build standalone/produção)
  return '10.135.60.38';
}

const PORTA_BACKEND = 3000;
export const API_URL = `http://${obterIpDoComputador()}:${PORTA_BACKEND}`;

const api = axios.create({
  baseURL: `${API_URL}/api`,
});

export default api;