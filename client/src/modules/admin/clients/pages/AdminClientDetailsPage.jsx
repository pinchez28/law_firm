import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';

import adminClientsService from '@/modules/admin/clients/services/adminClientsService';
import StatsCard from '@/components/ui/StatsCard';
import SectionHeading from '@/components/ui/SectionHeading';

import BackLink from '@/components/ui/BackLink';
import { formatDateTime } from '@/core/utils/dateFormatter';

const clientKeys = {
  detail: (id) => ['admin-client', id],
};

const AdminClientDetailsPage = () => {
  const { id } = useParams();

  const {
    data: client,
    isLoading,
    error,
  } = useQuery({
    queryKey: clientKeys.detail(id),
    queryFn: async () => {
      const response = await adminClientsService.getClientDetails(id);
      return response.data;
    },
    enabled: !!id,
  });

  if (isLoading) {
    return <div>Loading client details...</div>;
  }

  if (error) {
    return <div>Failed to load client details.</div>;
  }

  if (!client) {
    return <div>Client not found.</div>;
  }

  const analytics = client.analytics || {};
  const caseActivity = client.case_activity || {};
  const assignment = client.assignment || {};
  const cases = client.cases || [];
  const safeEmail = (email) => email || 'Has no email';
  const safeUserId = (id) => id || 'Has no user ID';

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 16 }}>
        <BackLink label='Back to Clients' fallbackPath='/admin/clients' />
      </div>
      <SectionHeading title='Client Full Details Page' />
      {/* CLIENT HEADER */}
      <div
        style={{
          marginBottom: 24,
          padding: 20,
          border: '1px solid #e5e7eb',
          borderRadius: 12,
        }}
      >
        <h2 style={{ marginBottom: 8 }}>{client.full_name}</h2>

        <p>
          <strong>Email:</strong> {safeEmail(client.email)}
        </p>

        <p>
          <strong>Phone:</strong> {client.phone_number}
        </p>

        <p>
          <strong>Client Type:</strong> {client.client_type}
        </p>

        <p>
          <strong>Status:</strong> {client.lifecycle_status}
        </p>

        <p>
          <strong>Portal Enabled:</strong>{' '}
          {client.portal_enabled ? 'Yes' : 'No'}
        </p>

        <p>
          <strong>Portal Client:</strong>{' '}
          {client.is_portal_client ? 'Yes' : 'No'}
        </p>

        <p>
          <strong>Active:</strong> {client.is_active ? 'Yes' : 'No'}
        </p>

        <p>
          <strong>Client ID:</strong> {client.client_id}
        </p>

        <p>
          <strong>User ID:</strong> {safeUserId(client.user_id)}
        </p>

        <p>
          <strong>Created:</strong> {formatDateTime(client.created_at)}
        </p>
      </div>

      {/* ANALYTICS */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: 12,
          marginBottom: 24,
        }}
      >
        <StatsCard title='Total Cases' value={analytics.total_cases || 0} />

        <StatsCard title='Pending' value={analytics.pending_cases || 0} />

        <StatsCard
          title='In Progress'
          value={analytics.in_progress_cases || 0}
        />

        <StatsCard title='Closed' value={analytics.closed_cases || 0} />

        <StatsCard title='Archived' value={analytics.archived_cases || 0} />
      </div>

      {/* CASE ACTIVITY */}
      <section
        style={{
          marginBottom: 24,
          padding: 20,
          border: '1px solid #e5e7eb',
          borderRadius: 12,
        }}
      >
        <h3>Case Activity</h3>

        <p>
          <strong>New Cases (30 Days):</strong>{' '}
          {caseActivity.new_cases_last_30_days || 0}
        </p>

        <p>
          <strong>Stale Cases:</strong> {caseActivity.stale_cases || 0}
        </p>

        <p>
          <strong>Last Case Created:</strong>{' '}
          {caseActivity.last_case_created_at
            ? formatDateTime(caseActivity.last_case_created_at)
            : 'N/A'}
        </p>
      </section>

      {/* ASSIGNMENT */}
      <section
        style={{
          marginBottom: 24,
          padding: 20,
          border: '1px solid #e5e7eb',
          borderRadius: 12,
        }}
      >
        <h3>Assignment</h3>

        <p>
          <strong>Assigned Cases:</strong> {assignment.assigned_cases || 0}
        </p>

        <p>
          <strong>Unassigned Cases:</strong> {assignment.unassigned_cases || 0}
        </p>

        <p>
          <strong>Lawyers Involved:</strong> {assignment.lawyers_involved || 0}
        </p>

        <p>
          <strong>Primary Lawyer:</strong>{' '}
          {assignment.primary_lawyer
            ?.assigned_lawyer__user__profile__full_name || 'Not Assigned'}
        </p>
      </section>

      {/* INSIGHTS */}
      <section
        style={{
          marginBottom: 24,
          padding: 20,
          border: '1px solid #e5e7eb',
          borderRadius: 12,
        }}
      >
        <h3>Insights</h3>

        {client.insights?.length ? (
          client.insights.map((insight, index) => (
            <div key={index}>• {insight}</div>
          ))
        ) : (
          <p>No insights available</p>
        )}
      </section>

      {/* CASES */}
      <section
        style={{
          padding: 20,
          border: '1px solid #e5e7eb',
          borderRadius: 12,
        }}
      >
        <h3>Cases</h3>

        {cases.length === 0 ? (
          <p>No cases found</p>
        ) : (
          cases.map((c, index) => (
            <div
              key={c.id || index}
              style={{
                padding: 12,
                marginBottom: 10,
                border: '1px solid #e5e7eb',
                borderRadius: 8,
              }}
            >
              <div>
                <strong>{c.title || c.case_title}</strong>
              </div>

              <div>Status: {c.status}</div>

              {c.case_number && <div>Case Number: {c.case_number}</div>}
            </div>
          ))
        )}
      </section>
    </div>
  );
};

export default AdminClientDetailsPage;
