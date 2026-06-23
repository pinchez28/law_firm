import axiosInstance from '@/core/api/axios';

const clientCasesService = {
  async getMyCases(params = {}) {
    const { data } = await axiosInstance.get('/cases/client/cases/', {
      params,
    });

    // backend returns: { success, message, data: [] }
    return data;
  },

  async getMyCaseById(caseId) {
    const { data } = await axiosInstance.get(`/cases/client/cases/${caseId}/`);

    // backend returns: { success, message, data: {...} }
    return data.data; // unwrap actual case object
  },
};

export default clientCasesService;
