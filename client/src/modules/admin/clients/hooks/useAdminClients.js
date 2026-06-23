import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import adminClientsService from '@/modules/admin/clients/services/adminClientsService';

/* =========================================================
   QUERY KEYS
========================================================= */
const CLIENTS_KEY = ['admin-clients'];

/* =========================================================
   FETCH CLIENTS
========================================================= */
const fetchClients = async (params = {}) => {
  return await adminClientsService.getClients(params);
};

/* =========================================================
   HOOK
========================================================= */
export const useAdminClients = (params = {}) => {
  const queryClient = useQueryClient();

  /* =========================================================
     GET CLIENTS
  ========================================================= */
  const { data, isLoading, isError, error, refetch, isFetching } = useQuery({
    queryKey: [...CLIENTS_KEY, params],
    queryFn: () => fetchClients(params),
  });

  /* =========================================================
     CREATE PORTAL CLIENT
  ========================================================= */
  const createPortalClient = useMutation({
    mutationFn: (payload) => adminClientsService.createPortalClient(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: CLIENTS_KEY,
      });
    },
  });

  /* =========================================================
     CREATE ASSISTED CLIENT
  ========================================================= */
  const createAssistedClient = useMutation({
    mutationFn: (payload) => adminClientsService.createAssistedClient(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: CLIENTS_KEY,
      });
    },
  });

  /* =========================================================
     DELETE PORTAL CLIENT
  ========================================================= */
  const deleteClient = useMutation({
    mutationFn: (clientId) => adminClientsService.deleteClient(clientId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: CLIENTS_KEY,
      });
    },
  });

  /* =========================================================
     TOGGLE OFFICIAL CLIENT STATUS
  ========================================================= */
  const toggleClientStatus = useMutation({
    mutationFn: (clientId) => adminClientsService.toggleClientStatus(clientId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: CLIENTS_KEY,
      });
    },
  });

  /* =========================================================
     RETURN API
  ========================================================= */
  return {
    summary: data?.analytics || {
      total_clients: 0,
      active_clients: 0,
      inactive_clients: 0,
      portal_enabled_clients: 0,
      assisted_clients: 0,
    },

    clients: data?.results || [],

    isLoading,
    isError,
    error,
    isFetching,
    refetch,

    /* Portal Client Creation */
    createPortalClient: createPortalClient.mutateAsync,
    isCreatingPortalClient: createPortalClient.isPending,

    /* Assisted Client Creation */
    createAssistedClient: createAssistedClient.mutateAsync,
    isCreatingAssistedClient: createAssistedClient.isPending,

    /* Permanent Delete */
    deleteClient: deleteClient.mutateAsync,
    isDeleting: deleteClient.isPending,

    /* Activate / Deactivate Official Client */
    toggleClientStatus: toggleClientStatus.mutateAsync,
    isTogglingClient: toggleClientStatus.isPending,
  };
};

export default useAdminClients;
