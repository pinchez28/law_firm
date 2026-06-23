import axiosInstance from '@/core/api/axios';

/* =========================================================
   ADMIN STAFF SERVICE
========================================================= */
const adminStaffService = {
  /* ======================================================
     STAFF LIST
  ====================================================== */
  async getStaff() {
    const { data } = await axiosInstance.get('/auth/staff/');
    return data;
  },

  /* ======================================================
     STAFF DETAILS
  ====================================================== */
  async getStaffDetails(userId) {
    const { data } = await axiosInstance.get(`/auth/staff/${userId}/`);
    return data;
  },

  /* ======================================================
     CREATE STAFF
  ====================================================== */
  // async createStaff(payload) {
  //   const { data } = await axiosInstance.post('/auth/staff/create/', payload);

  //   return data;
  // },

  async createStaff(payload) {
    try {
      const { data } = await axiosInstance.post('/auth/staff/create/', payload);

      return data;
    } catch (error) {
      console.log('CREATE STAFF ERROR');
      console.log(error.response?.data);
      console.log(error.response?.data?.errors?.phone_number);

      throw error;
    }
  },

  /* ======================================================
     UPDATE PERMISSIONS
  ==================================================== */
  async updateStaffPermissions(userId, payload) {
    const { data } = await axiosInstance.patch(
      `/auth/staff/${userId}/permissions/`,
      payload,
    );

    return data;
  },

  /* ======================================================
     TOGGLE STATUS
  ====================================================== */
  async toggleStaffStatus(userId) {
    const { data } = await axiosInstance.post(
      `/auth/staff/${userId}/toggle-status/`,
    );

    return data;
  },

  /* ======================================================
     DELETE STAFF
  ====================================================== */
  async deleteStaff(userId) {
    const { data } = await axiosInstance.delete(
      `/auth/staff/${userId}/delete/`,
    );

    return data;
  },
};

export default adminStaffService;
