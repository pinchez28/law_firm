import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Swal from 'sweetalert2';

import Card from '@/components/ui/Card';
import Button3D from '@/components/ui/Button3D';
import SectionHeading from '@/components/ui/SectionHeading';
import FloatingInput from '@/components/ui/FloatingInput';
import Select3D from '@/components/ui/Select3D';

import { useAdminClients } from '@/modules/admin/clients/hooks/useAdminClients';

export default function AdminCreateClientPage() {
  const navigate = useNavigate();
  const { createClient } = useAdminClients();

  const [searchParams] = useSearchParams();

  const clientType = (searchParams.get('type') || 'INDIVIDUAL').toUpperCase();
  const clientMode = searchParams.get('mode'); // portal | assisted | null

  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    email: '',
    phone_number: '',

    full_name: '',
    national_id: '',
    gender: '',
    occupation: '',
    marital_status: '',

    company_name: '',
    registration_number: '',
    incorporation_date: '',
    country_of_incorporation: '',
    industry: '',
    company_status: 'ACTIVE',

    contact_full_name: '',
    contact_email: '',
    contact_phone_number: '',
    contact_national_id_number: '',
    contact_role_or_designation: '',

    country: 'Kenya',
    county: '',
    city: '',
    street: '',
    postal_code: '',
    full_address: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const buildPayload = () => {
    const base = {
      email: formData.email,
      phone_number: formData.phone_number,
      country: formData.country,
      county: formData.county,
      city: formData.city,
      street: formData.street,
      postal_code: formData.postal_code,
      full_address: formData.full_address,
    };

    if (clientType === 'COMPANY') {
      return {
        ...base,
        company_name: formData.company_name,
        registration_number: formData.registration_number,
        incorporation_date: formData.incorporation_date || null,
        country_of_incorporation: formData.country_of_incorporation,
        industry: formData.industry,
        company_status: formData.company_status,
        contact_full_name: formData.contact_full_name,
        contact_email: formData.contact_email,
        contact_phone_number: formData.contact_phone_number,
        contact_national_id_number: formData.contact_national_id_number,
        contact_role_or_designation: formData.contact_role_or_designation,
      };
    }

    return {
      ...base,
      full_name: formData.full_name,
      national_id: formData.national_id,
      gender: formData.gender,
      occupation: formData.occupation,
      marital_status: formData.marital_status,

      client_type: clientType.toLowerCase(),
      client_mode: clientMode || 'standard',
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setIsSubmitting(true);

      const payload = buildPayload();
      const response = await createClient(payload, clientType);

      await Swal.fire({
        icon: 'success',
        title: 'Client Created Successfully',
        confirmButtonText: 'Continue',
        confirmButtonColor: '#2563eb',
      });

      navigate('/admin/clients');
    } catch (error) {
      const data = error?.response?.data;

      let html = `<p>${data?.message ?? 'Unable to create client'}</p>`;

      if (data?.errors) {
        html += "<ul style='text-align:left;margin-top:10px'>";
        Object.entries(data.errors).forEach(([field, errors]) => {
          html += `<li><b>${field}</b>: ${errors.join(', ')}</li>`;
        });
        html += '</ul>';
      }

      Swal.fire({
        icon: 'error',
        title: 'Creation Failed',
        html,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const isIndividual = clientType === 'INDIVIDUAL';
  const isCompany = clientType === 'COMPANY';

  return (
    <div className='space-y-6 p-4 md:p-6 animate-fadeIn'>
      <SectionHeading
        title='Create Client'
        subtitle={`${clientType}${clientMode ? ` / ${clientMode}` : ''}`}
      />

      <Card className='p-6'>
        <form onSubmit={handleSubmit} className='space-y-6'>
          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <FloatingInput
              label='Email'
              name='email'
              value={formData.email}
              onChange={handleChange}
            />

            <FloatingInput
              label='Phone Number'
              name='phone_number'
              value={formData.phone_number}
              onChange={handleChange}
            />
          </div>

          {isCompany && (
            <>
              <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                <FloatingInput
                  label='Company Name'
                  name='company_name'
                  value={formData.company_name}
                  onChange={handleChange}
                  required
                />

                <FloatingInput
                  label='Registration Number'
                  name='registration_number'
                  value={formData.registration_number}
                  onChange={handleChange}
                  required
                />
              </div>

              <FloatingInput
                label='Incorporation Date'
                name='incorporation_date'
                type='date'
                value={formData.incorporation_date}
                onChange={handleChange}
              />

              <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                <FloatingInput
                  label='Country of Incorporation'
                  name='country_of_incorporation'
                  value={formData.country_of_incorporation}
                  onChange={handleChange}
                />

                <FloatingInput
                  label='Industry'
                  name='industry'
                  value={formData.industry}
                  onChange={handleChange}
                />
              </div>

              <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                <FloatingInput
                  label='Contact Full Name'
                  name='contact_full_name'
                  value={formData.contact_full_name}
                  onChange={handleChange}
                  required
                />

                <FloatingInput
                  label='Contact Email'
                  name='contact_email'
                  value={formData.contact_email}
                  onChange={handleChange}
                  required
                />

                <FloatingInput
                  label='Contact Phone'
                  name='contact_phone_number'
                  value={formData.contact_phone_number}
                  onChange={handleChange}
                />

                <FloatingInput
                  label='Contact National ID'
                  name='contact_national_id_number'
                  value={formData.contact_national_id_number}
                  onChange={handleChange}
                  required
                />

                <FloatingInput
                  label='Contact Role'
                  name='contact_role_or_designation'
                  value={formData.contact_role_or_designation}
                  onChange={handleChange}
                />
              </div>
            </>
          )}

          {isIndividual && (
            <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
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
              />

              <Select3D
                label='Gender'
                name='gender'
                value={formData.gender}
                onChange={handleChange}
                options={[
                  { value: 'MALE', label: 'Male' },
                  { value: 'FEMALE', label: 'Female' },
                ]}
              />

              <FloatingInput
                label='Occupation'
                name='occupation'
                value={formData.occupation}
                onChange={handleChange}
              />

              <Select3D
                label='Marital Status'
                name='marital_status'
                value={formData.marital_status}
                onChange={handleChange}
                options={[
                  { value: 'SINGLE', label: 'Single' },
                  { value: 'MARRIED', label: 'Married' },
                  { value: 'DIVORCED', label: 'Divorced' },
                  { value: 'WIDOWED', label: 'Widowed' },
                ]}
              />
            </div>
          )}

          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <FloatingInput
              label='Country'
              name='country'
              value={formData.country}
              onChange={handleChange}
            />

            <FloatingInput
              label='County'
              name='county'
              value={formData.county}
              onChange={handleChange}
            />

            <FloatingInput
              label='City'
              name='city'
              value={formData.city}
              onChange={handleChange}
            />

            <FloatingInput
              label='Street'
              name='street'
              value={formData.street}
              onChange={handleChange}
            />

            <FloatingInput
              label='Postal Code'
              name='postal_code'
              value={formData.postal_code}
              onChange={handleChange}
            />

            <FloatingInput
              label='Full Address'
              name='full_address'
              value={formData.full_address}
              onChange={handleChange}
              required
            />
          </div>

          <div className='flex gap-3 pt-4'>
            <Button3D
              type='button'
              variant='secondary'
              onClick={() => navigate('/admin/clients')}
            >
              Cancel
            </Button3D>

            <Button3D type='submit' variant='primary' disabled={isSubmitting}>
              {isSubmitting ? 'Creating...' : 'Create Client'}
            </Button3D>
          </div>
        </form>
      </Card>
    </div>
  );
}
