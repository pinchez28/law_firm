import axiosInstance from '@/core/api/axios';

const adminCasesService = {
  async getCases(params = {}) {
    const { data } = await axiosInstance.get('/cases/', { params });
    return data;
  },

  async getCaseById(id) {
    const { data } = await axiosInstance.get(`/cases/${id}/`);
    return data;
  },

  async createCase(payload) {
    const { data } = await axiosInstance.post('/cases/create/', payload);
    return data;
  },

  async reassignLawyer(caseId, membershipId) {
    const { data } = await axiosInstance.patch(
      `/cases/${caseId}/reassign-lawyer/`,
      {
        membership_id: membershipId,
      },
    );

    return data;
  },

  async getLawyers() {
    const { data } = await axiosInstance.get('/admin/staff/lawyers/');
    return {
      ...data,
      data: {
        lawyers: data.lawyers || [],
      },
    };
  },

  async getSecretaries() {
    const { data } = await axiosInstance.get('/auth/staff/secretaries/');
    return data;
  },

  async getCaseSummary() {
    const { data } = await axiosInstance.get('/cases/');
    return data.summary;
  },

  async getLawyerPerformance() {
    const { data } = await axiosInstance.get('/cases/');
    return data.lawyer_performance;
  },

  async getTopClients() {
    const { data } = await axiosInstance.get('/cases/');
    return data.top_clients;
  },

  async getCasesList() {
    const { data } = await axiosInstance.get('/cases/');
    return data.cases;
  },
};

export default adminCasesService;
