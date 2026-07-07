import React from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  Building2,
  FolderTree,
  Landmark,
  ShieldCheck,
  Sparkles,
  Users,
} from 'lucide-react';

import adminFirmService from '@/modules/admin/firm/services/adminFirmService';

import Card from '@/components/ui/Card';
import StatsCard from '@/components/ui/StatsCard';
import Swal from '@/core/utils/themedSwal';
import { getApiErrorMessage } from '@/core/utils/errorMessages';

const timezoneOptions = {
  'Africa/Nairobi': 'Africa/Nairobi',
  UTC: 'UTC',
};

const languageOptions = {
  English: 'English',
  Swahili: 'Swahili',
};

const currencyOptions = {
  KES: 'KES',
  USD: 'USD',
  EUR: 'EUR',
  GBP: 'GBP',
};

function SectionTitle({ title, subtitle }) {
  return (
    <div>
      <h2 className='text-xl font-semibold text-gray-900 dark:text-white'>
        {title}
      </h2>
      {subtitle && (
        <p className='mt-1 text-sm text-gray-500 dark:text-gray-400'>
          {subtitle}
        </p>
      )}
    </div>
  );
}

function formatValue(value) {
  if (value === true) return 'Yes';
  if (value === false) return 'No';
  if (value === null || value === undefined || value === '') return 'Not set';
  return value;
}

function FieldRow({ label, value, onUpdate, multiline = false }) {
  return (
    <div className='grid gap-3 border-b border-border-light py-4 last:border-b-0 dark:border-border-dark md:grid-cols-[220px_1fr_auto] md:items-start'>
      <p className='text-sm font-semibold text-gray-500 dark:text-gray-400'>
        {label}
      </p>
      <p
        className={`text-sm font-medium text-gray-900 dark:text-white ${
          multiline ? 'whitespace-pre-line leading-6' : ''
        }`}
      >
        {formatValue(value)}
      </p>
      {onUpdate && (
        <button
          type='button'
          onClick={onUpdate}
          className='w-fit rounded-lg border border-brand-primary px-3 py-2 text-sm font-semibold text-brand-primary transition hover:bg-brand-primary hover:text-white'
        >
          Update
        </button>
      )}
    </div>
  );
}

export default function AdminFirmPage() {
  const queryClient = useQueryClient();

  const firmQuery = useQuery({
    queryKey: ['admin-firm'],
    queryFn: adminFirmService.getFirm,
  });

  const settingsQuery = useQuery({
    queryKey: ['admin-firm-settings'],
    queryFn: adminFirmService.getSettings,
  });

  const departmentsQuery = useQuery({
    queryKey: ['admin-firm-departments'],
    queryFn: adminFirmService.getDepartments,
  });

  const firmMutation = useMutation({
    mutationFn: adminFirmService.updateFirm,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-firm'] });
      Swal.fire({
        icon: 'success',
        title: 'Firm updated',
        timer: 1600,
        showConfirmButton: false,
      });
    },
    onError: (error) => {
      Swal.fire({
        icon: 'error',
        title: 'Update failed',
        text: getApiErrorMessage(
          error,
          'Could not update firm profile right now.',
        ),
      });
    },
  });

  const settingsMutation = useMutation({
    mutationFn: adminFirmService.updateSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-firm-settings'] });
      Swal.fire({
        icon: 'success',
        title: 'Settings updated',
        timer: 1600,
        showConfirmButton: false,
      });
    },
    onError: (error) => {
      Swal.fire({
        icon: 'error',
        title: 'Update failed',
        text: getApiErrorMessage(
          error,
          'Could not update firm settings right now.',
        ),
      });
    },
  });

  const departmentMutation = useMutation({
    mutationFn: ({ action, id, payload }) => {
      if (action === 'create') {
        return adminFirmService.createDepartment(payload);
      }

      if (action === 'delete') {
        return adminFirmService.deleteDepartment(id);
      }

      return adminFirmService.updateDepartment(id, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-firm'] });
      queryClient.invalidateQueries({ queryKey: ['admin-firm-departments'] });
      Swal.fire({
        icon: 'success',
        title: 'Department updated',
        timer: 1500,
        showConfirmButton: false,
      });
    },
    onError: (error) => {
      Swal.fire({
        icon: 'error',
        title: 'Department action failed',
        text: getApiErrorMessage(
          error,
          'Could not complete the department action.',
        ),
      });
    },
  });

  const updateFirmField = async ({
    field,
    label,
    value,
    input = 'text',
    required = false,
  }) => {
    const result = await Swal.fire({
      title: `Update ${label}`,
      input,
      inputValue: value || '',
      inputPlaceholder: label,
      showCancelButton: true,
      confirmButtonText: 'Update',
      inputValidator: (newValue) => {
        if (required && !String(newValue || '').trim()) {
          return `${label} is required`;
        }
        return null;
      },
    });

    if (!result.isConfirmed) return;

    firmMutation.mutate({
      [field]: result.value,
    });
  };

  const updateSettingField = async ({
    field,
    label,
    value,
    input = 'text',
    inputOptions,
    parser = (newValue) => newValue,
  }) => {
    const result = await Swal.fire({
      title: `Update ${label}`,
      input,
      inputValue: value ?? '',
      inputOptions,
      showCancelButton: true,
      confirmButtonText: 'Update',
    });

    if (!result.isConfirmed) return;

    settingsMutation.mutate({
      [field]: parser(result.value),
    });
  };

  const toggleSettingField = async ({ field, label, value }) => {
    const result = await Swal.fire({
      title: `${value ? 'Disable' : 'Enable'} ${label}?`,
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: value ? 'Disable' : 'Enable',
    });

    if (!result.isConfirmed) return;

    settingsMutation.mutate({
      [field]: !value,
    });
  };

  const toggleFirmActive = async (firm) => {
    const result = await Swal.fire({
      title: firm.is_active ? 'Deactivate firm?' : 'Activate firm?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: firm.is_active ? 'Deactivate' : 'Activate',
    });

    if (!result.isConfirmed) return;

    firmMutation.mutate({
      is_active: !firm.is_active,
    });
  };

  const openDepartmentForm = async (department = null) => {
    const result = await Swal.fire({
      title: department ? 'Update Department' : 'Add Department',
      html: `
        <input id="department-name" class="swal2-input" placeholder="Department name">
        <textarea id="department-description" class="swal2-textarea" placeholder="Description"></textarea>
      `,
      showCancelButton: true,
      confirmButtonText: department ? 'Update' : 'Create',
      didOpen: () => {
        const popup = Swal.getPopup();
        popup.querySelector('#department-name').value = department?.name || '';
        popup.querySelector('#department-description').value =
          department?.description || '';
      },
      preConfirm: () => {
        const popup = Swal.getPopup();
        const name = popup.querySelector('#department-name').value.trim();
        const description = popup
          .querySelector('#department-description')
          .value.trim();

        if (!name) {
          Swal.showValidationMessage('Department name is required');
          return false;
        }

        return { name, description };
      },
    });

    if (!result.isConfirmed) return;

    departmentMutation.mutate({
      action: department ? 'update' : 'create',
      id: department?.id,
      payload: result.value,
    });
  };

  const toggleDepartmentStatus = async (department) => {
    const result = await Swal.fire({
      title: department.is_active
        ? 'Disable department?'
        : 'Enable department?',
      text: department.is_active
        ? 'This department will stop appearing as an active option.'
        : 'This department will become available again.',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: department.is_active ? 'Disable' : 'Enable',
    });

    if (!result.isConfirmed) return;

    departmentMutation.mutate({
      action: 'update',
      id: department.id,
      payload: { is_active: !department.is_active },
    });
  };

  const deleteDepartment = async (department) => {
    const result = await Swal.fire({
      title: 'Delete department?',
      text: `${department.name} will be permanently removed.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Delete',
      confirmButtonColor: '#d33',
    });

    if (!result.isConfirmed) return;

    departmentMutation.mutate({
      action: 'delete',
      id: department.id,
    });
  };

  if (firmQuery.isLoading || settingsQuery.isLoading) {
    return (
      <div className='flex min-h-[420px] items-center justify-center'>
        Loading firm workspace...
      </div>
    );
  }

  if (firmQuery.error || settingsQuery.error) {
    return (
      <div className='flex min-h-[420px] items-center justify-center'>
        Failed to load firm management.
      </div>
    );
  }

  const firm = firmQuery.data?.firm ?? {};
  const settings = settingsQuery.data ?? {};
  const analytics = firmQuery.data?.analytics ?? {};
  const staffSummary = analytics.staff_summary ?? {};
  const organizationSummary = analytics.organization_summary ?? {};
  const firmInsights = analytics.firm_insights ?? {};
  const departments = departmentsQuery.data ?? [];

  return (
    <div className='space-y-8'>
      <div>
        <p className='text-sm font-semibold uppercase tracking-wide text-brand-primary'>
          Admin Management
        </p>
        <h1 className='mt-2 text-3xl font-bold text-gray-900 dark:text-white'>
          Firm
        </h1>
        <p className='mt-2 max-w-3xl text-gray-600 dark:text-gray-300'>
          Review firm details and update only the specific item that needs to
          change.
        </p>
      </div>

      <div className='grid gap-4 md:grid-cols-2 xl:grid-cols-4'>
        <StatsCard
          title='Active Staff'
          value={staffSummary.active_members ?? 0}
          subtitle={`${staffSummary.total_members ?? 0} total members`}
          icon={<Users size={22} />}
          color='blue'
        />
        <StatsCard
          title='Departments'
          value={organizationSummary.departments ?? departments.length}
          subtitle={`${organizationSummary.branches ?? 0} branches`}
          icon={<FolderTree size={22} />}
          color='green'
        />
        <StatsCard
          title='Practice Areas'
          value={organizationSummary.practice_areas ?? 0}
          subtitle={organizationSummary.structure_type || 'Not set'}
          icon={<Landmark size={22} />}
          color='yellow'
        />
        <StatsCard
          title='Firm Stage'
          value={firmInsights.maturity_stage || 'Not set'}
          subtitle={`Complexity: ${firmInsights.complexity_level || 'not set'}`}
          icon={<Building2 size={22} />}
          color='red'
        />
      </div>

      <Card className='p-6'>
        <div className='mb-2'>
          <SectionTitle
            title='Firm Profile'
            subtitle='Firm identity and public contact information.'
          />
        </div>

        <FieldRow
          label='Firm Name'
          value={firm.name}
          onUpdate={() =>
            updateFirmField({
              field: 'name',
              label: 'Firm Name',
              value: firm.name,
              required: true,
            })
          }
        />
        <FieldRow label='Registration Number' value={firm.registration_number} />
        <FieldRow
          label='KRA PIN'
          value={firm.kra_pin}
          onUpdate={() =>
            updateFirmField({
              field: 'kra_pin',
              label: 'KRA PIN',
              value: firm.kra_pin,
            })
          }
        />
        <FieldRow
          label='Email'
          value={firm.email}
          onUpdate={() =>
            updateFirmField({
              field: 'email',
              label: 'Email',
              value: firm.email,
              input: 'email',
            })
          }
        />
        <FieldRow
          label='Phone Number'
          value={firm.phone_number}
          onUpdate={() =>
            updateFirmField({
              field: 'phone_number',
              label: 'Phone Number',
              value: firm.phone_number,
            })
          }
        />
        <FieldRow
          label='Website'
          value={firm.website}
          onUpdate={() =>
            updateFirmField({
              field: 'website',
              label: 'Website',
              value: firm.website,
              input: 'url',
            })
          }
        />
        <FieldRow
          label='Postal Address'
          value={firm.postal_address}
          onUpdate={() =>
            updateFirmField({
              field: 'postal_address',
              label: 'Postal Address',
              value: firm.postal_address,
            })
          }
        />
        <FieldRow
          label='Physical Address'
          value={firm.physical_address}
          multiline
          onUpdate={() =>
            updateFirmField({
              field: 'physical_address',
              label: 'Physical Address',
              value: firm.physical_address,
              input: 'textarea',
            })
          }
        />
        <FieldRow
          label='Description'
          value={firm.description}
          multiline
          onUpdate={() =>
            updateFirmField({
              field: 'description',
              label: 'Description',
              value: firm.description,
              input: 'textarea',
            })
          }
        />
        <FieldRow
          label='Firm Active'
          value={firm.is_active}
          onUpdate={() => toggleFirmActive(firm)}
        />
        <FieldRow label='Owner' value={firm.owner_name} />
        <FieldRow label='Owner Email' value={firm.owner_email} />
      </Card>

      <Card className='p-6'>
        <div className='mb-2'>
          <SectionTitle
            title='Firm Settings'
            subtitle='Operating rules, portal behavior, security, and AI options.'
          />
        </div>

        <FieldRow
          label='Timezone'
          value={settings.timezone}
          onUpdate={() =>
            updateSettingField({
              field: 'timezone',
              label: 'Timezone',
              value: settings.timezone,
              input: 'select',
              inputOptions: timezoneOptions,
            })
          }
        />
        <FieldRow
          label='Language'
          value={settings.language}
          onUpdate={() =>
            updateSettingField({
              field: 'language',
              label: 'Language',
              value: settings.language,
              input: 'select',
              inputOptions: languageOptions,
            })
          }
        />
        <FieldRow
          label='Currency'
          value={settings.currency}
          onUpdate={() =>
            updateSettingField({
              field: 'currency',
              label: 'Currency',
              value: settings.currency,
              input: 'select',
              inputOptions: currencyOptions,
            })
          }
        />
        <FieldRow
          label='Opening Time'
          value={settings.opening_time}
          onUpdate={() =>
            updateSettingField({
              field: 'opening_time',
              label: 'Opening Time',
              value: settings.opening_time,
              input: 'text',
            })
          }
        />
        <FieldRow
          label='Closing Time'
          value={settings.closing_time}
          onUpdate={() =>
            updateSettingField({
              field: 'closing_time',
              label: 'Closing Time',
              value: settings.closing_time,
              input: 'text',
            })
          }
        />
        <FieldRow
          label='Session Timeout Minutes'
          value={settings.session_timeout_minutes}
          onUpdate={() =>
            updateSettingField({
              field: 'session_timeout_minutes',
              label: 'Session Timeout Minutes',
              value: settings.session_timeout_minutes,
              input: 'number',
              parser: (newValue) => Number(newValue) || 60,
            })
          }
        />
        {[
          ['work_on_saturday', 'Work On Saturday'],
          ['work_on_sunday', 'Work On Sunday'],
          ['email_notifications', 'Email Notifications'],
          ['sms_notifications', 'SMS Notifications'],
          ['browser_notifications', 'Browser Notifications'],
          ['allow_client_registration', 'Allow Client Registration'],
          ['allow_client_document_upload', 'Allow Client Document Upload'],
          ['allow_client_case_tracking', 'Allow Client Case Tracking'],
          ['require_password_change', 'Require Password Change'],
          ['enable_two_factor_authentication', 'Two Factor Authentication'],
          ['enable_ai_assistant', 'AI Assistant'],
          ['enable_ai_case_suggestions', 'AI Case Suggestions'],
          ['enable_ai_deadline_reminders', 'AI Deadline Reminders'],
          ['is_active', 'Firm Settings Active'],
        ].map(([field, label]) => (
          <FieldRow
            key={field}
            label={label}
            value={settings[field]}
            onUpdate={() =>
              toggleSettingField({
                field,
                label,
                value: settings[field],
              })
            }
          />
        ))}
      </Card>

      <div className='grid gap-6 xl:grid-cols-[1.2fr_0.8fr]'>
        <Card className='p-6'>
          <div className='mb-5 flex flex-col gap-4 md:flex-row md:items-center md:justify-between'>
            <div className='flex items-center gap-3'>
              <FolderTree className='text-brand-primary' size={24} />
              <SectionTitle
                title='Departments'
                subtitle='Create, update, disable, or remove firm departments.'
              />
            </div>
            <button
              type='button'
              onClick={() => openDepartmentForm()}
              className='w-fit rounded-lg bg-brand-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700'
            >
              Add Department
            </button>
          </div>

          <div className='overflow-hidden rounded-xl border border-border-light dark:border-border-dark'>
            <table className='w-full text-left text-sm'>
              <thead className='bg-gray-50 text-gray-600 dark:bg-gray-800 dark:text-gray-300'>
                <tr>
                  <th className='px-4 py-3 font-semibold'>Name</th>
                  <th className='px-4 py-3 font-semibold'>Description</th>
                  <th className='px-4 py-3 font-semibold'>Branch</th>
                  <th className='px-4 py-3 font-semibold'>Status</th>
                  <th className='px-4 py-3 text-right font-semibold'>Actions</th>
                </tr>
              </thead>
              <tbody className='divide-y divide-border-light dark:divide-border-dark'>
                {departments.length > 0 ? (
                  departments.map((department) => (
                    <tr key={department.id}>
                      <td className='px-4 py-3 text-gray-900 dark:text-white'>
                        {department.name}
                      </td>
                      <td className='max-w-xs px-4 py-3 text-gray-600 dark:text-gray-300'>
                        {department.description || 'Not set'}
                      </td>
                      <td className='px-4 py-3 text-gray-600 dark:text-gray-300'>
                        {department.branch_name || 'Main firm'}
                      </td>
                      <td className='px-4 py-3'>
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-semibold ${
                            department.is_active
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-gray-200 text-gray-700'
                          }`}
                        >
                          {department.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className='px-4 py-3'>
                        <div className='flex flex-wrap justify-end gap-2'>
                          <button
                            type='button'
                            onClick={() => openDepartmentForm(department)}
                            className='rounded-lg border border-brand-primary px-3 py-1.5 text-xs font-semibold text-brand-primary transition hover:bg-brand-primary hover:text-white'
                          >
                            Update
                          </button>
                          <button
                            type='button'
                            onClick={() => toggleDepartmentStatus(department)}
                            className='rounded-lg border border-yellow-600 px-3 py-1.5 text-xs font-semibold text-yellow-700 transition hover:bg-yellow-600 hover:text-white'
                          >
                            {department.is_active ? 'Disable' : 'Enable'}
                          </button>
                          <button
                            type='button'
                            onClick={() => deleteDepartment(department)}
                            className='rounded-lg border border-red-600 px-3 py-1.5 text-xs font-semibold text-red-600 transition hover:bg-red-600 hover:text-white'
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan='5'
                      className='px-4 py-8 text-center text-gray-500'
                    >
                      No departments found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>

        <Card className='p-6'>
          <div className='mb-5 flex items-center gap-3'>
            <ShieldCheck className='text-brand-primary' size={24} />
            <SectionTitle
              title='Role Breakdown'
              subtitle='Active firm structure by system role.'
            />
          </div>

          <div className='space-y-3'>
            {Object.entries(staffSummary.by_role || {}).length > 0 ? (
              Object.entries(staffSummary.by_role).map(([role, count]) => (
                <div
                  key={role}
                  className='flex items-center justify-between rounded-xl border border-border-light px-4 py-3 dark:border-border-dark'
                >
                  <span className='font-medium text-gray-900 dark:text-white'>
                    {role.replace(/_/g, ' ')}
                  </span>
                  <span className='rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-700'>
                    {count}
                  </span>
                </div>
              ))
            ) : (
              <p className='rounded-xl border border-border-light px-4 py-6 text-center text-gray-500 dark:border-border-dark'>
                No role breakdown available.
              </p>
            )}
          </div>

          <div className='mt-6 rounded-xl border border-border-light p-4 dark:border-border-dark'>
            <div className='flex items-center gap-3'>
              <Sparkles size={20} className='text-brand-primary' />
              <div>
                <p className='font-semibold text-gray-900 dark:text-white'>
                  Engagement Health
                </p>
                <p className='text-sm text-gray-500 dark:text-gray-400'>
                  {staffSummary.engagement_health || 'No data'}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
