import axiosInstance from '@/core/api/axios';

const lawyerCommunicationService = {
  async getNotifications(params = {}) {
    const { data } = await axiosInstance.get('/staff/lawyer/notifications/', {
      params,
    });
    return data;
  },
};

export default lawyerCommunicationService;
