import { useState } from 'react';
import adminCasesService from '@/modules/admin/cases/services/adminCasesService';
import Swal from '@/core/utils/themedSwal';

export default function useCreateCase() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const createCase = async (payload, onSuccess) => {
    try {
      setLoading(true);
      setError(null);

      const result = await adminCasesService.createCase(payload);

      await Swal.fire({
        icon: 'success',
        title: 'Success',
        text: 'Case created successfully',
        timer: 2000,
        showConfirmButton: false,
      });

      if (onSuccess) onSuccess(result);
      return result;
    } catch (err) {
      setError(err);

      Swal.fire({
        icon: 'error',
        title: 'Error',
        text:
          err?.response?.data?.message ||
          err?.response?.data?.errors?.[0] ||
          'Failed to create case',
      });

      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    createCase,
    loading,
    error,
  };
}
