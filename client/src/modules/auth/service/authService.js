import axiosInstance from '@/core/api/axios';

const authService = {
  // =====================
  // AUTH
  // =====================
  async login(payload) {
    const { data } = await axiosInstance.post('auth/login/', payload);
    return data;
  },

  async register(payload) {
    const { data } = await axiosInstance.post('/auth/register/', payload);
    return data;
  },

  // =====================
  // PASSWORD FLOW
  // =====================
  async forgotPassword(payload) {
    const { data } = await axiosInstance.post(
      '/auth/forgot-password/',
      payload,
    );
    return data;
  },

  async resetPassword(payload) {
    const { data } = await axiosInstance.post('/auth/reset-password/', payload);
    return data;
  },

  // =====================
  // TOKEN
  // =====================
  async refreshToken(payload) {
    const { data } = await axiosInstance.post('/auth/token/refresh/', payload);
    return data;
  },

  // =====================
  // ACCOUNT RECOVERY
  // =====================
  async recoverAccount(payload) {
    const { data } = await axiosInstance.post(
      '/auth/recover-account/',
      payload,
    );
    return data;
  },

  // =====================
  // LOGOUT
  // =====================
  async logout(payload) {
    const { data } = await axiosInstance.post('/auth/logout/', payload);
    return data;
  },
};

export default authService;
