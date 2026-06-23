import axiosInstance from '@/core/api/axios';

const lawyerCasesService = {
  async getMyCases(params = {}) {
    const { data } = await axiosInstance.get('/cases/my-cases/', { params });

    return data; // array directly
  },

  async getMyCaseById(caseId) {
    const { data } = await axiosInstance.get(`/cases/my-cases/${caseId}/`);

    return data.data; // 👈 IMPORTANT FIX (unwrap backend)
  },
};

export default lawyerCasesService;
