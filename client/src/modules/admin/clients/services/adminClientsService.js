import axiosInstance from '@/core/api/axios';

/* =========================================================
   ADMIN CLIENTS SERVICE
========================================================= */
const adminClientsService = {
  // ======================================================
  // CLIENT CREATION
  // ======================================================
  async createPortalClient(payload) {
    const { data } = await axiosInstance.post(
      '/auth/clients/portal/create/',
      payload,
    );

    return data;
  },

  async createAssistedClient(payload) {
    const { data } = await axiosInstance.post(
      '/auth/clients/assisted/create/',
      payload,
    );

    return data;
  },
  // ======================================================
  // CLIENT LISTING
  // ======================================================
  async getClients(params = {}) {
    const { data } = await axiosInstance.get('/auth/clients/', {
      params,
    });

    return data;
  },

  async getClientDetails(clientId) {
    const { data } = await axiosInstance.get(`/auth/clients/${clientId}/`);

    return data;
  },

  // ======================================================
  // CLIENT STATUS
  // ======================================================
  async toggleClientStatus(clientId) {
    const { data } = await axiosInstance.post(
      `/auth/clients/${clientId}/toggle-status/`,
    );

    return data;
  },

  // ======================================================
  // CLIENT DELETE
  // ======================================================
  async deleteClient(clientId) {
    const { data } = await axiosInstance.delete(
      `/auth/clients/${clientId}/delete/`,
    );

    return data;
  },

  // ======================================================
  // CLIENT CASES
  // ======================================================
  async getClientCases(clientId, params = {}) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/cases/`,
      { params },
    );

    return data;
  },

  // ======================================================
  // CLIENT DOCUMENTS
  // ======================================================
  async getClientDocuments(clientId, params = {}) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/documents/`,
      { params },
    );

    return data;
  },

  // ======================================================
  // CLIENT COMMUNICATION
  // ======================================================
  async getClientCommunication(clientId, params = {}) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/communication/`,
      { params },
    );

    return data;
  },

  // ======================================================
  // CLIENT BILLING
  // ======================================================
  async getClientBilling(clientId) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/billing/`,
    );

    return data;
  },

  async getClientInvoices(clientId) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/invoices/`,
    );

    return data;
  },

  async getClientPayments(clientId) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/payments/`,
    );

    return data;
  },

  // ======================================================
  // CLIENT ACTIVITY
  // ======================================================
  async getClientActivity(clientId, params = {}) {
    const { data } = await axiosInstance.get(
      `/auth/clients/${clientId}/activity/`,
      { params },
    );

    return data;
  },

  // ======================================================
  // CLIENT UPDATE
  // ======================================================
  async updateClient(clientId, payload) {
    const { data } = await axiosInstance.patch(
      `/auth/clients/${clientId}/`,
      payload,
    );

    return data;
  },
};

export default adminClientsService;
