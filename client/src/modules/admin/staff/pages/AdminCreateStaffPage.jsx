import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Swal from 'sweetalert2';

import Card from '@/components/ui/Card';
import Button3D from '@/components/ui/Button3D';
import SectionHeading from '@/components/ui/SectionHeading';
import FloatingInput from '@/components/ui/FloatingInput';

import { useAdminStaff } from '@/modules/admin/staff/hooks/useAdminStaff';

export default function AdminCreateStaffPage() {
  const navigate = useNavigate();

  const { createStaff } = useAdminStaff();

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
      permissions: prev.permissions.includes(permission)
        ? prev.permissions.filter((p) => p !== permission)
        : [...prev.permissions, permission],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('SUBMIT CLICKED');

    try {
      setIsSubmitting(true);

      if (formData.firm_role !== 'LAWYER') {
        throw new Error('Only lawyer creation is connected at the moment.');
      }

      await createStaff(formData);

      await Swal.fire({
        icon: 'success',
        title: 'Success',
        text: 'Staff created successfully.',
        timer: 2000,
        showConfirmButton: false,
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
            </select>
          </div>

          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <FloatingInput
              label='Admission Number'
              name='admission_number'
              value={formData.admission_number}
              onChange={handleChange}
              required
            />

            <FloatingInput
              label='Date Hired'
              type='date'
              name='date_hired'
              value={formData.date_hired}
              onChange={handleChange}
              required
            />

            <FloatingInput
              label='Department'
              name='department'
              value={formData.department}
              onChange={handleChange}
            />

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
