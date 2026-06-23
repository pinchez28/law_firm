import { useState } from 'react';

import AuthContext from '@/core/store/AuthContext';
import {
  clearAuthSession,
  getStoredAuth,
  saveAuthSession,
} from '@/core/utils/authStorage';

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      return getStoredAuth().user;
    } catch (error) {
      console.error('Failed to parse user:', error);
      return null;
    }
  });

  const [accessToken, setAccessToken] = useState(
    () => getStoredAuth().accessToken,
  );

  const [refreshToken, setRefreshToken] = useState(
    () => getStoredAuth().refreshToken,
  );

  const login = ({ user, access, refresh }, rememberMe = true) => {
    setUser(user);
    setAccessToken(access);
    setRefreshToken(refresh);

    saveAuthSession({ user, access, refresh }, rememberMe);
  };

  const logout = () => {
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);

    clearAuthSession();
  };

  // =========================
  // ROLE HELPERS (ADD THIS)
  // =========================
  const role = user?.role;
  const firmRole = user?.firm_role;

  const isAdmin = role === 'ADMIN';
  const isClient = role === 'CLIENT';
  const isStaff = role === 'STAFF';

  const isLawyer = firmRole === 'LAWYER';
  const isSecretary = firmRole === 'SECRETARY';

  const value = {
    user,
    accessToken,
    refreshToken,

    login,
    logout,

    isAuthenticated: !!accessToken,

    // roles
    role,
    firmRole,

    // helpers
    isAdmin,
    isClient,
    isStaff,
    isLawyer,
    isSecretary,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
