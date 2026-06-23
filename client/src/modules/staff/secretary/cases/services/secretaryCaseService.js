import axiosInstance from '@/core/api/axios';

const secretaryCasesService = {
  // LIST
  async getMyCases(params = {}) {
    const { data } = await axiosInstance.get('/cases/secretary/cases/', {
      params,
    });

    return data;
  },

  // DETAIL
  async getMyCaseById(caseId) {
    const { data } = await axiosInstance.get(
      `/cases/secretary/cases/${caseId}/`,
    );

    return data.data;
  },

  // CREATE (NEW SECRETARY ENDPOINT)
  async createCase(payload) {
    const { data } = await axiosInstance.post(
      '/cases/secretary/cases/create/',
      payload,
    );

    return data;
  },
};

export default secretaryCasesService;
