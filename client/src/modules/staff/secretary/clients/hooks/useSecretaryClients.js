import { useEffect, useState } from 'react';
import axiosInstance from '@/core/api/axios';

export function useSecretaryClients() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const res = await axiosInstance.get('/auth/secretary/clients/');

        setClients(res.data || []);
      } catch {
        setClients([]);
      } finally {
        setLoading(false);
      }
    };

    fetchClients();
  }, []);

  return { clients, loading };
}
