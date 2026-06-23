import { useState } from 'react';

import { saveAuthSession } from '@/core/utils/authStorage';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShieldCheck, Lock, ArrowLeft } from 'lucide-react';

import useAuth from '@/modules/auth/hook/useAuth';
import AuthContext from '@/core/store/AuthContext';
import { useContext } from 'react';

import Card from '@/components/ui/Card';
import Button3D from '@/components/ui/Button3D';
import FloatingInput from '@/components/ui/FloatingInput';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const { login, loading, error } = useAuth();
  const { login: authLogin } = useContext(AuthContext);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const data = await login({ email, password });

      if (!data) throw new Error('Invalid login response');

      const { user, access, refresh } = data;

      if (!user || !access || !refresh) {
        throw new Error('Invalid login response from server');
      }

      /* =====================================================
         TOKEN STORAGE (single, consistent auth source)
      ===================================================== */
      saveAuthSession({ user, access, refresh }, rememberMe);

      /* =====================================================
         AUTH CONTEXT UPDATE (UI state only)
      ===================================================== */
      authLogin({ user, access, refresh }, rememberMe);

      /* =====================================================
         ROLE ROUTING
      ===================================================== */
      const role = user.role;
      const firmRole = user.firm_role;

      if (role === 'ADMIN') return navigate('/admin/dashboard');

      if (role === 'CLIENT') {
        if (!firmRole) return navigate('/portal/dashboard');
        if (firmRole === 'CLIENT') return navigate('/client/dashboard');
        return navigate('/');
      }

      if (role === 'STAFF') {
        if (firmRole === 'LAWYER') return navigate('/lawyer/dashboard');
        if (firmRole === 'SECRETARY') return navigate('/secretary/dashboard');
        return navigate('/');
      }

      navigate('/');
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div className='flex-1 flex flex-col lg:flex-row'>
      {/* LEFT PANEL */}
      <div className='hidden lg:flex lg:w-1/2 bg-blue-700 relative items-center justify-center p-10 overflow-hidden'>
        <motion.div
          animate={{ scale: [1, 1.2, 1], x: [0, 40, 0], y: [0, -30, 0] }}
          transition={{ duration: 8, repeat: Infinity }}
          className='absolute w-96 h-96 bg-blue-500/40 rounded-full blur-3xl'
        />

        <div className='relative text-center text-white max-w-md'>
          <ShieldCheck size={90} className='mx-auto mb-6' />
          <h1 className='text-4xl font-bold mb-4'>Secure Legal Access</h1>
          <p className='text-blue-100'>
            Login to manage cases, documents, and communication securely.
          </p>
        </div>
      </div>

      {/* RIGHT PANEL */}
      <div className='w-full lg:w-1/2 flex items-center justify-center px-6 py-24 bg-gray-50'>
        <Card className='w-full max-w-md p-8'>
          <Link
            to='/'
            className='flex items-center gap-2 text-sm text-blue-600 mb-6'
          >
            <ArrowLeft size={16} />
            Back to Home
          </Link>

          <div className='flex items-center gap-2 mb-6'>
            <Lock className='text-blue-600' />
            <h2 className='text-2xl font-bold'>Login</h2>
          </div>

          <form onSubmit={handleLogin} className='space-y-5'>
            <FloatingInput
              label='Email'
              type='email'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <FloatingInput
              label='Password'
              type='password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            {/* =====================================================
               REMEMBER ME (NOW FUNCTIONAL)
            ===================================================== */}
            <div className='flex justify-between text-sm'>
              <label className='flex items-center gap-2 text-gray-800'>
                <input
                  type='checkbox'
                  checked={rememberMe}
                  onChange={() => setRememberMe(!rememberMe)}
                />
                Remember me
              </label>

              <div className='flex flex-col items-end gap-1'>
                {/* NORMAL PASSWORD RESET FLOW */}
                <Link
                  to='/forgot-password'
                  className='text-blue-700 hover:underline'
                >
                  Forgot password?
                </Link>

                {/* ACCOUNT RECOVERY FLOW (NEW) */}
                <Link
                  to='/recover-account'
                  className='text-gray-600 hover:text-blue-700 text-xs'
                >
                  Can’t access your email?
                </Link>
              </div>
            </div>

            <Button3D type='submit' className='w-full' disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </Button3D>

            {/* ERROR */}
            {error && (
              <p className='text-red-500 text-center text-sm'>
                {error?.response?.data?.message ||
                  error?.message ||
                  'Login failed'}
              </p>
            )}

            <p className='text-sm text-center mt-6 text-gray-600'>
              Don’t have an account?{' '}
              <Link to='/register' className='text-blue-600 font-bold'>
                Create account
              </Link>
            </p>
          </form>
        </Card>
      </div>
    </div>
  );
}
