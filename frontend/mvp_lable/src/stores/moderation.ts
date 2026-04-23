import { defineStore } from 'pinia';

// Определяем типы для строгости и автодополнения
interface UserInfo {
  id: number;
  name: string;
}

export interface ReleaseForModeration {
  id: number;
  title: string;
  status: 'pending' | 'approved' | 'rejected' | 'published' | 'draft';
  owner: UserInfo;
  image?: string;
  release_date: string;
  created_at: string;
  // Добавьте другие поля, которые нужны модератору для принятия решения
}

interface ModerationState {
  releases: ReleaseForModeration[];
  isLoading: boolean;
  error: string | null;
}

export const useModerationStore = defineStore('moderation', {
  // 1. СОСТОЯНИЕ (State)
  // Здесь хранятся данные, которые мы получаем с сервера
  state: (): ModerationState => ({
    releases: [],       // Список релизов в очереди на модерацию
    isLoading: false,   // Флаг для отображения индикатора загрузки
    error: null,        // Для хранения сообщений об ошибках
  }),

  // 2. ГЕТТЕРЫ (Getters)
  // Это как вычисляемые свойства (computed) для вашего стора
  getters: {
    pendingCount(state): number {
      return state.releases.length;
    },
  },

  // 3. ДЕЙСТВИЯ (Actions)
  // Методы для взаимодействия с API и изменения состояния
  actions: {
    // Получение очереди релизов со статусом 'pending'
    async fetchQueue() {
      this.isLoading = true;
      this.error = null;
      try {
        // TODO: Замените на ваш реальный API-запрос
        // const response = await api.get('/moderation/queue');
        // this.releases = response.data;

        // --- Mock-данные для симуляции ---
        await new Promise(res => setTimeout(res, 1000));
        this.releases = [
            { id: 1, title: 'Cybernetic Dreams', status: 'pending', owner: { id: 10, name: 'SynthRider' }, created_at: '2026-04-21T10:00:00Z', release_date: '2026-05-01T00:00:00Z' },
            { id: 2, title: 'Neon Pulse', status: 'pending', owner: { id: 12, name: 'GridRunner' }, created_at: '2026-04-22T12:30:00Z', release_date: '2026-05-05T00:00:00Z' },
        ];
        // --- Конец Mock-данных ---

      } catch (e: any) {
        this.error = 'Failed to load moderation queue.';
        console.error(e);
      } finally {
        this.isLoading = false;
      }
    },

    // Одобрение релиза
    async approveRelease(releaseId: number) {
      try {
        // TODO: Замените на ваш реальный API-запрос
        // await api.post(`/moderation/releases/${releaseId}/approve`);

        // Оптимистичное обновление: удаляем из списка сразу, не дожидаясь перезагрузки
        this.releases = this.releases.filter(r => r.id !== releaseId);

      } catch (e: any) {
        // В случае ошибки можно показать уведомление
        console.error(`Failed to approve release ${releaseId}`, e);
        // Можно добавить логику возвращения релиза в список, если нужно
      }
    },

    // Отклонение релиза
    async rejectRelease(releaseId: number, reason: string) {
      if (!reason) return;
      try {
        // TODO: Замените на ваш реальный API-запрос
        // await api.post(`/moderation/releases/${releaseId}/reject`, { reason });

        // Так же оптимистично удаляем из списка
        this.releases = this.releases.filter(r => r.id !== releaseId);

      } catch (e: any) {
        console.error(`Failed to reject release ${releaseId}`, e);
      }
    },
  },
});