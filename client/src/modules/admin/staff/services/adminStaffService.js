import axiosInstance from '@/core/api/axios';

/* =========================================================
   ADMIN STAFF SERVICE
========================================================= */
const adminStaffService = {
  /* ======================================================
     STAFF LIST
  ====================================================== */
  async getStaff() {
    const { data } = await axiosInstance.get('/admin/staff/lawyers/');
    const lawyers = data.lawyers || [];
    const metadata = data.metadata || {};

    return {
      data: {
        summary: {
          total_staff: metadata.total_records ?? lawyers.length,
          active_staff: metadata.summary?.active ?? 0,
          inactive_staff: metadata.summary?.inactive ?? 0,
          lawyers: metadata.total_records ?? lawyers.length,
          secretaries: 0,
          total_active_cases: 0,
          total_closed_cases: 0,
        },
        staff: lawyers.map((lawyer) => ({
          ...lawyer,
          user_id: lawyer.id,
          role: lawyer.firm_role || 'LAWYER',
          workload: {
            level: 'N/A',
            active_cases: 0,
            closed_cases: 0,
            total_cases: 0,
          },
        })),
      },
    };
  },

  /* ======================================================
     STAFF DETAILS
  ====================================================== */
  async getStaffDetails(userId) {
    const { data } = await axiosInstance.get(`/admin/staff/lawyers/${userId}/`);
    const lawyer = data.lawyer || {};

    return {
      data: {
        user: {
          full_name: lawyer.full_name,
          email: lawyer.email,
          system_role: 'STAFF',
          firm_role: lawyer.firm_role,
          status: lawyer.employment_status,
          is_active: lawyer.is_active,
          is_verified: true,
          phone_number: lawyer.phone_number,
          national_id: lawyer.national_id_number,
          created_at: lawyer.created_at,
        },
        membership: {
          role: lawyer.firm_role,
          is_active: lawyer.is_active,
        },
        permissions: [],
        available_permissions: [],
        workload: {
          active_cases: 0,
          closed_cases: 0,
          total_cases: 0,
        },
        recent_cases: [],
        lawyer,
      },
    };
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
      const nameParts = (payload.full_name || '').trim().split(/\s+/);
      const firstName = payload.first_name || nameParts[0] || '';
      const lastName =
        payload.last_name || nameParts.slice(1).join(' ') || '-';

      const requestPayload = {
        first_name: firstName,
        last_name: lastName,
        email: payload.email,
        phone_number: payload.phone_number,
        national_id_number: payload.national_id || payload.national_id_number,
        staff_number: payload.staff_number || undefined,
        employee_number: payload.employee_number || undefined,
        department: payload.department || '',
        job_title: payload.job_title || 'Lawyer',
        work_email: payload.work_email || payload.email,
        work_phone: payload.work_phone || payload.phone_number,
        office_location: payload.office_location || '',
        admission_number: payload.admission_number,
        practicing_certificate_number:
          payload.practicing_certificate_number || '',
        bar_admission_date: payload.bar_admission_date || null,
        is_notary: Boolean(payload.is_notary),
        can_commission_oaths: Boolean(payload.can_commission_oaths),
        is_court_approved: payload.is_court_approved ?? true,
        employment_type: payload.employment_type || 'PERMANENT',
        date_hired: payload.date_hired,
        probation_end_date: payload.probation_end_date || null,
        professional_summary: payload.professional_summary || '',
      };

      const { data } = await axiosInstance.post(
        '/admin/staff/lawyers/create/',
        requestPayload,
      );

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
      `/admin/staff/lawyers/${userId}/update/`,
      payload,
    );

    return data;
  },

  /* ======================================================
     TOGGLE STATUS
  ====================================================== */
  async toggleStaffStatus(userId) {
    const details = await this.getStaffDetails(userId);
    const isActive = details.data?.lawyer?.is_active;
    const action = isActive ? 'deactivate' : 'activate';
    const { data } = await axiosInstance.post(
      `/admin/staff/lawyers/${userId}/${action}/`,
    );

    return data;
  },

  /* ======================================================
     DELETE STAFF
  ====================================================== */
  async deleteStaff(userId) {
    const { data } = await axiosInstance.delete(
      `/admin/staff/lawyers/${userId}/delete/`,
    );

    return data;
  },
};

export default adminStaffService;
