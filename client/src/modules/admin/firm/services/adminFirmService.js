import axiosInstance from '@/core/api/axios';

const adminFirmService = {
  async getFirm() {
    const { data } = await axiosInstance.get('/admin/firm/');
    return data;
  },

  async updateFirm(payload) {
    const { data } = await axiosInstance.patch('/admin/firm/', payload);
    return data;
  },

  async getSettings() {
    const { data } = await axiosInstance.get('/admin/firm/settings/');
    return data;
  },

  async updateSettings(payload) {
    const { data } = await axiosInstance.patch('/admin/firm/settings/', payload);
    return data;
  },

  async getDepartments() {
    const { data } = await axiosInstance.get('/admin/firm/departments/');
    return data.departments || [];
  },

  async createDepartment(payload) {
    const { data } = await axiosInstance.post('/admin/firm/departments/', payload);
    return data;
  },

  async updateDepartment(id, payload) {
    const { data } = await axiosInstance.patch(
      `/admin/firm/departments/${id}/`,
      payload,
    );
    return data;
  },

  async deleteDepartment(id) {
    await axiosInstance.delete(`/admin/firm/departments/${id}/`);
  },
};

export default adminFirmService;
