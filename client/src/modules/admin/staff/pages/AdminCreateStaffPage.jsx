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
    password: '',
    firm_role: 'SECRETARY',
    permissions: [],
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
        text: error?.response?.data?.message || 'Failed to create staff.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const availablePermissions = [
    'manage_cases',
    'schedule_events',
    'manage_documents',
    'manage_clients',
  ];

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

          <FloatingInput
            label='Password'
            type='password'
            name='password'
            value={formData.password}
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
              <option value='SECRETARY'>Secretary</option>
            </select>
          </div>

          <div>
            <label className='block text-sm font-medium mb-3'>
              Permissions
            </label>

            <div className='grid grid-cols-1 md:grid-cols-2 gap-3'>
              {availablePermissions.map((permission) => (
                <label key={permission} className='flex items-center gap-2'>
                  <input
                    type='checkbox'
                    checked={formData.permissions.includes(permission)}
                    onChange={() => handlePermissionChange(permission)}
                  />

                  <span>{permission.replaceAll('_', ' ')}</span>
                </label>
              ))}
            </div>
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
