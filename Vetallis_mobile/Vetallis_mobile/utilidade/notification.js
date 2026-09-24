import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';
import { Platform } from 'react-native';
import { API_URL } from '../src/services/api';

export async function registrarPushToken(usuarioId) {
  if (!Device.isDevice) {
    console.log('Push notifications só funcionam em dispositivo físico.');
    return;
  }

  const { status: statusAtual } = await Notifications.getPermissionsAsync();
  let status = statusAtual;

  if (status !== 'granted') {
    const { status: novoStatus } = await Notifications.requestPermissionsAsync();
    status = novoStatus;
  }

  if (status !== 'granted') {
    console.log('Permissão de notificação negada pelo usuário.');
    return;
  }

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
    });
  }

  const projectId = Constants?.expoConfig?.extra?.eas?.projectId;
  const { data: token } = await Notifications.getExpoPushTokenAsync(
    projectId ? { projectId } : undefined
  );

  try {
    await fetch(`${API_URL}/api/push-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuarioId, token }),
    });
  } catch (erro) {
    console.log('Erro ao registrar push token:', erro.message);
  }
}