import React from 'react';
import { Outlet } from 'react-router-dom';
import PublicNavbar from '@/layouts/public/PublicNavbar';
import Footer from '@/components/shared/Footer';

const PublicLayout = () => {
  return (
    <div className='min-h-screen bg-[#050816] text-white flex flex-col'>
      {/* Navbar */}
      <PublicNavbar />

      {/* Page content */}
      <main className='pt-20 flex-1'>
        <Outlet />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default PublicLayout;
