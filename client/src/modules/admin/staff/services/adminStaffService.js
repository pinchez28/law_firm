import axiosInstance from '@/core/api/axios';

/* =========================================================
   ADMIN STAFF SERVICE
========================================================= */
const adminStaffService = {
  normalizeStaffMember(member, role) {
    return {
      ...member,
      user_id: member.id,
      role: member.firm_role || role,
      workload: {
        level: 'N/A',
        active_cases: 0,
        closed_cases: 0,
        total_cases: 0,
      },
    };
  },

  splitName(payload) {
    const nameParts = (payload.full_name || '').trim().split(/\s+/);
    return {
      first_name: payload.first_name || nameParts[0] || '',
      last_name: payload.last_name || nameParts.slice(1).join(' ') || '-',
    };
  },

  /* ======================================================
     STAFF LIST
  ====================================================== */
  async getStaff() {
    const [lawyerResponse, secretaryResponse] = await Promise.all([
      axiosInstance.get('/admin/staff/lawyers/'),
      axiosInstance.get('/admin/staff/secretaries/'),
    ]);

    const lawyers = lawyerResponse.data.lawyers || [];
    const secretaries = secretaryResponse.data.secretaries || [];
    const lawyerMetadata = lawyerResponse.data.metadata || {};
    const secretaryMetadata = secretaryResponse.data.metadata || {};
    const staff = [
      ...lawyers.map((lawyer) =>
        adminStaffService.normalizeStaffMember(lawyer, 'LAWYER'),
      ),
      ...secretaries.map((secretary) =>
        adminStaffService.normalizeStaffMember(secretary, 'SECRETARY'),
      ),
    ];

    return {
      data: {
        summary: {
          total_staff: staff.length,
          active_staff:
            (lawyerMetadata.summary?.active ?? 0) +
            (secretaryMetadata.summary?.active ?? 0),
          inactive_staff:
            (lawyerMetadata.summary?.inactive ?? 0) +
            (secretaryMetadata.summary?.inactive ?? 0),
          lawyers: lawyerMetadata.total_records ?? lawyers.length,
          secretaries: secretaryMetadata.total_records ?? secretaries.length,
          total_active_cases: 0,
          total_closed_cases: 0,
        },
        staff,
      },
    };
  },

  /* ======================================================
     STAFF DETAILS
  ====================================================== */
  async getStaffDetails(userId) {
    let staffMember;
    let role;

    try {
      const { data } = await axiosInstance.get(`/admin/staff/lawyers/${userId}/`);
      staffMember = data.lawyer || {};
      role = 'LAWYER';
    } catch (error) {
      if (error?.response?.status !== 404) throw error;
      const { data } = await axiosInstance.get(
        `/admin/staff/secretaries/${userId}/`,
      );
      staffMember = data.secretary || {};
      role = 'SECRETARY';
    }

    const availablePermissions = (staffMember.available_permissions || []).map(
      (permission) => ({
        code: permission.code,
        name: permission.name || permission.label || permission.code,
      }),
    );

    return {
      data: {
        user: {
          full_name: staffMember.full_name,
          email: staffMember.email,
          system_role: 'STAFF',
          firm_role: staffMember.firm_role || role,
          status: staffMember.employment_status,
          is_active: staffMember.is_active,
          is_verified: true,
          phone_number: staffMember.phone_number,
          national_id: staffMember.national_id_number,
          created_at: staffMember.created_at,
        },
        membership: {
          role: staffMember.firm_role || role,
          is_active: staffMember.is_active,
        },
        permissions: staffMember.permissions || [],
        available_permissions: availablePermissions,
        workload: {
          active_cases: 0,
          closed_cases: 0,
          total_cases: 0,
        },
        secretary_metrics: staffMember.analytics
          ? {
              assigned_tasks: 0,
              completed_tasks: 0,
              managed_appointments: 0,
              documents_processed: 0,
              assigned_lawyers: staffMember.analytics.assigned_lawyers || 0,
              active_permissions: staffMember.analytics.active_permissions || 0,
            }
          : {},
        recent_cases: [],
        recent_activity: [],
        lawyer: role === 'LAWYER' ? staffMember : null,
        secretary: role === 'SECRETARY' ? staffMember : null,
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
      const { first_name: firstName, last_name: lastName } =
        adminStaffService.splitName(payload);

      const basePayload = {
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
        employment_type: payload.employment_type || 'PERMANENT',
        date_hired: payload.date_hired,
        probation_end_date: payload.probation_end_date || null,
      };

      if (payload.firm_role === 'SECRETARY') {
        const secretaryPayload = {
          ...basePayload,
          job_title: payload.job_title || 'Secretary',
          can_prepare_documents: payload.can_prepare_documents ?? true,
          can_schedule_appointments: payload.can_schedule_appointments ?? true,
          can_manage_client_intake: payload.can_manage_client_intake ?? true,
          can_receive_documents: payload.can_receive_documents ?? true,
          permission_codes: payload.permission_codes || [],
          notes: payload.notes || '',
        };

        const { data } = await axiosInstance.post(
          '/admin/staff/secretaries/create/',
          secretaryPayload,
        );

        return data;
      }

      const lawyerPayload = {
        ...basePayload,
        job_title: payload.job_title || 'Lawyer',
        admission_number: payload.admission_number,
        practicing_certificate_number:
          payload.practicing_certificate_number || '',
        bar_admission_date: payload.bar_admission_date || null,
        is_notary: Boolean(payload.is_notary),
        can_commission_oaths: Boolean(payload.can_commission_oaths),
        is_court_approved: payload.is_court_approved ?? true,
        professional_summary: payload.professional_summary || '',
      };

      const { data } = await axiosInstance.post(
        '/admin/staff/lawyers/create/',
        lawyerPayload,
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
    const details = await adminStaffService.getStaffDetails(userId);
    const role = details.data?.membership?.role;
    const endpoint =
      role === 'SECRETARY'
        ? `/admin/staff/secretaries/${userId}/permissions/`
        : `/admin/staff/lawyers/${userId}/update/`;
    const body =
      role === 'SECRETARY'
        ? { permission_codes: payload.permissions || [] }
        : payload;

    const { data } = await axiosInstance[role === 'SECRETARY' ? 'post' : 'patch'](
      endpoint,
      body,
    );

    return data;
  },

  /* ======================================================
     TOGGLE STATUS
  ====================================================== */
  async toggleStaffStatus(staffMemberOrId) {
    const userId = staffMemberOrId?.user_id || staffMemberOrId?.id || staffMemberOrId;
    const role = staffMemberOrId?.role;
    const isActive = staffMemberOrId?.is_active;

    if (!role) {
      const details = await adminStaffService.getStaffDetails(userId);
      const resolvedRole = details.data?.membership?.role;
      const resolvedIsActive =
        details.data?.lawyer?.is_active ?? details.data?.secretary?.is_active;
      return adminStaffService.toggleStaffStatus({
        user_id: userId,
        role: resolvedRole,
        is_active: resolvedIsActive,
      });
    }

    const action = isActive ? 'deactivate' : 'activate';
    const segment = role === 'SECRETARY' ? 'secretaries' : 'lawyers';
    const { data } = await axiosInstance.post(
      `/admin/staff/${segment}/${userId}/${action}/`,
    );

    return data;
  },

  /* ======================================================
     DELETE STAFF
  ====================================================== */
  async deleteStaff(staffMemberOrId) {
    const userId = staffMemberOrId?.user_id || staffMemberOrId?.id || staffMemberOrId;
    const role = staffMemberOrId?.role;

    if (!role) {
      const details = await adminStaffService.getStaffDetails(userId);
      const resolvedRole = details.data?.membership?.role;
      return adminStaffService.deleteStaff({
        user_id: userId,
        role: resolvedRole,
      });
    }

    const segment = role === 'SECRETARY' ? 'secretaries' : 'lawyers';
    const { data } = await axiosInstance.delete(
      `/admin/staff/${segment}/${userId}/delete/`,
    );

    return data;
  },
};

export default adminStaffService;
