import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import Swal from 'sweetalert2';

import Card from '@/components/ui/Card';
import Button3D from '@/components/ui/Button3D';
import SectionHeading from '@/components/ui/SectionHeading';
import FloatingInput from '@/components/ui/FloatingInput';

import { useAdminClients } from '@/modules/admin/clients/hooks/useAdminClients';

const CLIENT_TYPES = [
  { value: 'INDIVIDUAL', label: 'Individual' },
  { value: 'COMPANY', label: 'Company' },
  { value: 'ORGANIZATION', label: 'Organization' },
  { value: 'GOVERNMENT', label: 'Government Entity' },
  { value: 'GROUP', label: 'Group of Persons' },
  { value: 'ESTATE', label: 'Estate / Deceased Estate' },
  { value: 'UNKNOWN', label: 'Not Classified' },
];

export default function AdminCreateClientPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { createPortalClient, createAssistedClient } = useAdminClients();

  const clientMode = searchParams.get('type') || 'portal';

  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    client_type: '',
    phone_number: '',
    national_id: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setIsSubmitting(true);

      if (clientMode === 'portal') {
        await createPortalClient({
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name,
          phone_number: formData.phone_number,
          national_id: formData.national_id,
          client_type: formData.client_type,
        });
      } else {
        await createAssistedClient({
          full_name: formData.full_name,
          national_id: formData.national_id,
          phone_number: formData.phone_number,
          client_type: formData.client_type,
        });
      }

      await Swal.fire({
        icon: 'success',
        title: 'Success',
        text:
          clientMode === 'portal'
            ? 'Portal client created successfully.'
            : 'Assisted client created successfully.',
        timer: 2000,
        showConfirmButton: false,
      });

      navigate('/admin/clients');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text:
          error?.response?.data?.message ||
          JSON.stringify(error?.response?.data?.errors) ||
          'Failed to create client.',
      });

      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className='space-y-6 p-4 md:p-6 animate-fadeIn'>
      <SectionHeading
        title={
          clientMode === 'portal'
            ? 'Create Portal Client'
            : 'Create Assisted Client'
        }
        subtitle='Add a new client to the system'
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

          <div className='space-y-2'>
            <label className='text-sm font-medium text-text-primary-light dark:text-text-primary-dark'>
              Client Type
            </label>

            <div className='relative'>
              <select
                name='client_type'
                value={formData.client_type}
                onChange={handleChange}
                required
                className='w-full appearance-none rounded-2xl border border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark text-text-primary-light dark:text-text-primary-dark px-4 py-3 pr-10 shadow-soft focus:outline-none focus:ring-2 focus:ring-brand-primary'
              >
                <option value=''>Select Client Type</option>

                <option value='INDIVIDUAL'>Individual</option>
                <option value='COMPANY'>Company</option>
                <option value='ORGANIZATION'>Organization</option>
                <option value='GOVERNMENT'>Government Entity</option>
                <option value='GROUP'>Group of Persons</option>
                <option value='ESTATE'>Estate / Deceased Estate</option>
                <option value='UNKNOWN'>Not Classified</option>
              </select>

              {/* dropdown arrow fix */}
              <div className='pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-text-muted-light dark:text-text-muted-dark'>
                ▼
              </div>
            </div>
          </div>

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

          {clientMode === 'portal' && (
            <>
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
            </>
          )}

          <div className='flex gap-3 pt-4'>
            <Button3D
              type='button'
              variant='secondary'
              onClick={() => navigate('/admin/clients')}
            >
              Cancel
            </Button3D>

            <Button3D type='submit' variant='primary' disabled={isSubmitting}>
              {isSubmitting
                ? 'Creating...'
                : clientMode === 'portal'
                  ? 'Create Portal Client'
                  : 'Create Assisted Client'}
            </Button3D>
          </div>
        </form>
      </Card>
    </div>
  );
}
