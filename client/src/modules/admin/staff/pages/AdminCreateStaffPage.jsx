import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';

import Swal from '@/core/utils/themedSwal';

import Card from '@/components/ui/Card';
import Button3D from '@/components/ui/Button3D';
import SectionHeading from '@/components/ui/SectionHeading';
import FloatingInput from '@/components/ui/FloatingInput';

import adminFirmService from '@/modules/admin/firm/services/adminFirmService';
import { useAdminStaff } from '@/modules/admin/staff/hooks/useAdminStaff';

export default function AdminCreateStaffPage() {
  const navigate = useNavigate();

  const { createStaff } = useAdminStaff();
  const { data: departments = [], isLoading: isLoadingDepartments } = useQuery({
    queryKey: ['admin-firm-departments'],
    queryFn: adminFirmService.getDepartments,
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '',
    national_id: '',
    phone_number: '',
    email: '',
    firm_role: 'LAWYER',
    department: '',
    job_title: 'Lawyer',
    staff_number: '',
    employee_number: '',
    work_email: '',
    work_phone: '',
    office_location: '',
    admission_number: '',
    practicing_certificate_number: '',
    bar_admission_date: '',
    employment_type: 'PERMANENT',
    date_hired: new Date().toISOString().slice(0, 10),
    professional_summary: '',
    can_prepare_documents: true,
    can_schedule_appointments: true,
    can_manage_client_intake: true,
    can_receive_documents: true,
    permission_codes: [],
    notes: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePermissionChange = (permission) => {
    setFormData((prev) => ({
      ...prev,
      permission_codes: prev.permission_codes.includes(permission)
        ? prev.permission_codes.filter((p) => p !== permission)
        : [...prev.permission_codes, permission],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('SUBMIT CLICKED');

    try {
      setIsSubmitting(true);

      const response = await createStaff(formData);
      const tempPassword = response?.temp_password;

      await Swal.fire({
        icon: 'success',
        title: 'Success',
        html: `
          <div style="text-align:left">
            <p>Staff created successfully.</p>
            ${
              tempPassword
                ? `
                  <div style="margin-top:12px;padding:12px;border-radius:8px;background:#f8fafc;border:1px solid #e2e8f0">
                    <p style="margin:0 0 6px 0"><strong>Temporary Password</strong></p>
                    <code style="font-size:16px;font-weight:700">${tempPassword}</code>
                  </div>
                  <p style="margin-top:10px;font-size:13px;color:#64748b">
                    Share this with the staff member. They will be required to change it after login.
                  </p>
                `
                : ''
            }
          </div>
        `,
        confirmButtonText: 'Continue',
        confirmButtonColor: '#2563eb',
      });

      navigate('/admin/staff');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text:
          error?.message ||
          error?.response?.data?.detail ||
          error?.response?.data?.message ||
          'Failed to create staff.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className='space-y-6 p-4 md:p-6 animate-fadeIn'>
      <SectionHeading
        title='Create Staff Member'
        subtitle='Add a lawyer or secretary to your firm'
      />

      <Card className='p-6'>
        <form onSubmit={handleSubmit} className='space-y-5'>
          <FloatingInput
            label='Full Name'
            name='full_name'
            value={formData.full_name}
            onChange={handleChange}
            required
          />

          <FloatingInput
            label='National ID'
            name='national_id'
            value={formData.national_id}
            onChange={handleChange}
            required
          />

          <FloatingInput
            label='Phone Number'
            name='phone_number'
            value={formData.phone_number}
            onChange={handleChange}
            required
          />

          <FloatingInput
            label='Email Address'
            type='email'
            name='email'
            value={formData.email}
            onChange={handleChange}
            required
          />

          <div>
            <label className='block text-sm font-medium mb-2'>Staff Role</label>

            <select
              value={formData.firm_role}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  firm_role: e.target.value,
                  job_title:
                    e.target.value === 'SECRETARY' ? 'Secretary' : 'Lawyer',
                })
              }
              className='
    w-full
    px-4 py-3
    rounded-xl
    border
    border-border-light
    dark:border-border-dark

    bg-surface-light
    dark:bg-surface-dark

    text-text-primary-light
    dark:text-text-primary-dark

    focus:outline-none
    focus:ring-2
    focus:ring-brand-primary
  '
            >
              <option value='LAWYER'>Lawyer</option>
              <option value='SECRETARY'>Secretary</option>
            </select>
          </div>

          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            {formData.firm_role === 'LAWYER' && (
              <FloatingInput
                label='Admission Number'
                name='admission_number'
                value={formData.admission_number}
                onChange={handleChange}
                required
              />
            )}

            <FloatingInput
              label='Date Hired'
              type='date'
              name='date_hired'
              value={formData.date_hired}
              onChange={handleChange}
              required
            />

            <div className='space-y-2'>
              <label
                htmlFor='department'
                className='block text-sm font-medium text-text-primary-light dark:text-text-primary-dark'
              >
                Department
              </label>

              <select
                id='department'
                name='department'
                value={formData.department}
                onChange={handleChange}
                disabled={isLoadingDepartments}
                className='
                  w-full h-12 rounded-2xl border border-border-light dark:border-border-dark
                  bg-surface-light dark:bg-surface-dark
                  text-text-primary-light dark:text-text-primary-dark
                  px-4 shadow-soft transition-all
                  focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary
                '
              >
                <option value=''>
                  {isLoadingDepartments
                    ? 'Loading departments...'
                    : 'Select department'}
                </option>

                {departments.map((department) => (
                  <option key={department.id} value={department.name}>
                    {department.name}
                  </option>
                ))}
              </select>
            </div>

            <FloatingInput
              label='Job Title'
              name='job_title'
              value={formData.job_title}
              onChange={handleChange}
            />

            <FloatingInput
              label='Staff Number'
              name='staff_number'
              value={formData.staff_number}
              onChange={handleChange}
            />

            <FloatingInput
              label='Employee Number'
              name='employee_number'
              value={formData.employee_number}
              onChange={handleChange}
            />

            <FloatingInput
              label='Work Email'
              type='email'
              name='work_email'
              value={formData.work_email}
              onChange={handleChange}
            />

            <FloatingInput
              label='Office Location'
              name='office_location'
              value={formData.office_location}
              onChange={handleChange}
            />
          </div>

          {formData.firm_role === 'SECRETARY' && (
            <div className='space-y-4 rounded-xl border border-border-light dark:border-border-dark p-4'>
              <h3 className='font-semibold'>Secretary Default Work</h3>

              <div className='grid grid-cols-1 md:grid-cols-2 gap-3'>
                {[
                  ['can_prepare_documents', 'Prepare Documents'],
                  ['can_schedule_appointments', 'Schedule Appointments'],
                  ['can_manage_client_intake', 'Manage Client Intake'],
                  ['can_receive_documents', 'Receive Documents'],
                ].map(([name, label]) => (
                  <label key={name} className='flex items-center gap-2'>
                    <input
                      type='checkbox'
                      checked={Boolean(formData[name])}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          [name]: e.target.checked,
                        }))
                      }
                    />
                    <span>{label}</span>
                  </label>
                ))}
              </div>

              <h3 className='font-semibold pt-2'>Extra Admin Permissions</h3>

              <div className='grid grid-cols-1 md:grid-cols-2 gap-3'>
                {[
                  ['MANAGE_CASES', 'Manage Cases'],
                  ['MANAGE_TASKS', 'Manage Tasks'],
                  ['MANAGE_CLIENTS', 'Manage Clients'],
                  ['MANAGE_DOCUMENTS', 'Manage Documents'],
                  ['MANAGE_CALENDAR', 'Manage Calendar'],
                  ['SEND_COMMUNICATIONS', 'Send Communications'],
                  ['VIEW_REPORTS', 'View Reports'],
                  ['MANAGE_BILLING', 'Manage Billing'],
                ].map(([code, label]) => (
                  <label key={code} className='flex items-center gap-2'>
                    <input
                      type='checkbox'
                      checked={formData.permission_codes.includes(code)}
                      onChange={() => handlePermissionChange(code)}
                    />
                    <span>{label}</span>
                  </label>
                ))}
              </div>

              <FloatingInput
                label='Notes'
                name='notes'
                value={formData.notes}
                onChange={handleChange}
              />
            </div>
          )}

          <div className='flex gap-3 pt-4'>
            <Button3D
              type='button'
              variant='secondary'
              onClick={() => navigate('/admin/staff')}
            >
              Cancel
            </Button3D>

            <Button3D type='submit' variant='primary' disabled={isSubmitting}>
              {isSubmitting ? 'Creating...' : 'Create Staff'}
            </Button3D>
          </div>
        </form>
      </Card>
    </div>
  );
}
