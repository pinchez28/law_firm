import React, { useContext } from 'react';

import LawyerLayout from '@/layouts/staff/lawyer/LawyerLayout';

import ThemeProvider from '@/core/store/ThemeProvider';

import AuthContext from '@/core/store/AuthContext';

export default function LawyerLayoutWrapper() {
  const { user } = useContext(AuthContext);

  return (
    <ThemeProvider
      key={`lawyer-${user?.user_id || user?.id || user?._id || user?.email}`}
      role='lawyer'
      user={user}
    >
      <LawyerLayout />
    </ThemeProvider>
  );
}
