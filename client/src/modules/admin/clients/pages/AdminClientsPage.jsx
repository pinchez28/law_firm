import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Swal from 'sweetalert2';

import { Users, UserCheck, UserPlus, Briefcase } from 'lucide-react';

import { useAdminClients } from '@/modules/admin/clients/hooks/useAdminClients';

import DataTable from '@/components/ui/DataTable';
import Card from '@/components/ui/Card';
import StatsCard from '@/components/ui/StatsCard';
import { Input3D } from '@/components/ui/Input3D';
import Button3D from '@/components/ui/Button3D';
import SectionHeading from '@/components/ui/SectionHeading';

export default function AdminClientsPage() {
  const navigate = useNavigate();

  const [search, setSearch] = useState('');

  const {
    clients,
    summary,
    isLoading,
    isFetching,
    refetch,
    deleteClient,
    toggleClientStatus,
  } = useAdminClients({ search });

  const handleToggleStatus = async (client) => {
    const activating = !client.is_active;

    const result = await Swal.fire({
      title: activating ? 'Activate Client?' : 'Deactivate Client?',
      text: activating
        ? 'This client will regain access to firm services.'
        : 'This client will be marked inactive but all cases will remain.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: activating ? 'Yes, activate' : 'Yes, deactivate',
    });

    if (!result.isConfirmed) return;

    try {
      await toggleClientStatus(client.client_id);

      Swal.fire({
        icon: 'success',
        title: 'Success',
        text: activating
          ? 'Client activated successfully'
          : 'Client deactivated successfully',
        timer: 2000,
        showConfirmButton: false,
      });
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text:
          error?.response?.data?.message || 'Failed to update client status',
      });
    }
  };

  const handleDelete = async (clientId) => {
    const result = await Swal.fire({
      title: 'Delete Client?',
      text: 'This client will be removed completely.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete',
      cancelButtonText: 'Cancel',
      confirmButtonColor: '#d33',
    });

    if (!result.isConfirmed) return;

    try {
      await deleteClient(clientId);

      Swal.fire({
        title: 'Success',
        text: 'Client deleted successfully',
        icon: 'success',
        timer: 2000,
        showConfirmButton: false,
      });
    } catch (error) {
      Swal.fire({
        title: 'Error',
        text: error?.response?.data?.message || 'Failed to delete client',
        icon: 'error',
      });
    }
  };

  const renderLifecycleStatus = (value) => {
    const styles = {
      PORTAL: 'bg-green-100 text-green-800',
      ASSISTED: 'bg-yellow-100 text-yellow-800',
      OFFICIAL: 'bg-purple-100 text-purple-800',
    };

    return (
      <span
        className={`px-2 py-1 rounded-full text-xs font-semibold ${
          styles[value] || 'bg-gray-100 text-gray-800'
        }`}
      >
        {value}
      </span>
    );
  };

  const renderClientType = (value) => {
    if (!value) return 'Not set';

    return value
      .replace(/_/g, ' ')
      .toLowerCase()
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  if (isLoading) {
    return (
      <div className='flex items-center justify-center min-h-[400px]'>
        <p className='text-text-muted-dark'>Loading clients...</p>
      </div>
    );
  }

  return (
    <div className='space-y-6 p-4 md:p-6 animate-fadeIn'>
      <div className='flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between'>
        <SectionHeading
          title='Client Management'
          subtitle='Manage All Clients'
        />

        <div className='flex flex-wrap gap-3'>
          <Button3D onClick={refetch}>
            {isFetching ? 'Refreshing...' : 'Refresh'}
          </Button3D>

          <Button3D
            variant='primary'
            onClick={() => navigate('/admin/clients/create?type=portal')}
          >
            + Portal Client
          </Button3D>

          <Button3D
            variant='secondary'
            onClick={() => navigate('/admin/clients/create?type=assisted')}
          >
            + Assisted Client
          </Button3D>
        </div>
      </div>

      <div className='grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-4'>
        <StatsCard
          title='Total Clients'
          value={summary?.total_clients ?? 0}
          icon={<Users size={22} />}
          color='blue'
        />

        <StatsCard
          title='Portal Clients'
          value={summary?.portal_clients ?? 0}
          icon={<UserCheck size={22} />}
          color='green'
        />

        <StatsCard
          title='Assisted Clients'
          value={summary?.assisted_clients ?? 0}
          icon={<UserPlus size={22} />}
          color='yellow'
        />

        <StatsCard
          title='Official Clients'
          value={summary?.official_clients ?? 0}
          icon={<Users size={22} />}
          color='purple'
        />

        <StatsCard
          title='Clients With Cases'
          value={summary?.clients_with_cases ?? 0}
          icon={<Briefcase size={22} />}
          color='red'
        />
      </div>

      <Card className='p-4'>
        <Input3D
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder='Search clients...'
        />
      </Card>

      <DataTable
        data={clients || []}
        mobileTitleKey='full_name'
        mobileSubtitleKey='phone_number'
        emptyMessage='No clients found.'
        columns={[
          {
            key: 'full_name',
            label: 'Name',
          },
          {
            key: 'email',
            label: 'Email',
            render: (value) => value || 'No portal account',
          },
          {
            key: 'phone_number',
            label: 'Phone',
            render: (value) => value || 'Not provided',
          },
          {
            key: 'client_type',
            label: 'Client Type',
            render: renderClientType,
          },
          {
            key: 'lifecycle_status',
            label: 'Lifecycle',
            render: renderLifecycleStatus,
          },
          {
            key: 'case_count',
            label: 'Cases',
            render: (value) => value ?? 0,
          },
          {
            key: 'is_active',
            label: 'Status',
            render: (value) => (
              <span
                className={
                  value
                    ? 'text-success font-semibold'
                    : 'text-error font-semibold'
                }
              >
                {value ? 'Active' : 'Inactive'}
              </span>
            ),
          },
        ]}
        actions={(client) => (
          <div className='flex flex-wrap gap-2'>
            <Button3D
              size='sm'
              onClick={() => navigate(`/admin/clients/${client.client_id}`)}
            >
              View
            </Button3D>

            {client.case_count === 0 && (
              <Button3D
                size='sm'
                variant='danger'
                onClick={() => handleDelete(client.client_id)}
              >
                Delete
              </Button3D>
            )}

            {client.case_count > 0 && (
              <Button3D
                size='sm'
                variant={client.is_active ? 'warning' : 'success'}
                onClick={() => handleToggleStatus(client)}
              >
                {client.is_active ? 'Deactivate' : 'Activate'}
              </Button3D>
            )}
          </div>
        )}
      />
    </div>
  );
}
