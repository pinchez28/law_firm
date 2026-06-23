import axiosInstance from '@/core/api/axios';

const secretaryClientsService = {
  async getClients(params = {}) {
    const { data } = await axiosInstance.get('/auth/secretary/clients/', {
      params,
    });

    return data;
  },

  async getClientById(clientId) {
    const { data } = await axiosInstance.get(
      `/auth/secretary/clients/${clientId}/`,
    );

    return data;
  },
};

export default secretaryClientsService;
