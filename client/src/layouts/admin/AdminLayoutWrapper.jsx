import React, { useContext } from 'react';

import AdminLayout from '@/layouts/admin/AdminLayout';

import ThemeProvider from '@/core/store/ThemeProvider';

import AuthContext from '@/core/store/AuthContext';

export default function AdminLayoutWrapper() {
  const { user } = useContext(AuthContext);

  return (
    <ThemeProvider
      key={`admin-${user?.user_id || user?.id || user?._id || user?.email}`}
      role='admin'
      user={user}
    >
      <AdminLayout />
    </ThemeProvider>
  );
}
