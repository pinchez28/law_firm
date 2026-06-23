import PublicNavbar from "@/layouts/public/PublicNavbar";
import Footer from "@/components/shared/Footer";
import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-900 via-blue-700 to-indigo-900 text-white">
      {/* Navbar */}
      <PublicNavbar variant="auth" />

      {/* AUTH CONTENT AREA */}
      <main className="flex-1 flex items-center justify-center px-4 py-10">
        <Outlet />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
