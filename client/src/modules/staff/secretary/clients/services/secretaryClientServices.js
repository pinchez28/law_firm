import axiosInstance from '@/core/api/axios';

const secretaryClientsService = {
  async getClients(params = {}) {
    const { data } = await axiosInstance.get('/staff/secretary/clients/', {
      params,
    });

    return data;
  },

  async getClientById(clientId) {
    const { clients } = await this.getClients();
    return clients.find((client) => String(client.id) === String(clientId));
  },
};

export default secretaryClientsService;
