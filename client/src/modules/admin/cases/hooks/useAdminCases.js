import { useEffect, useState } from 'react';
import adminCasesService from '@/modules/admin/cases/services/adminCasesService';

export default function useAdminCases() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCases = async () => {
      try {
        setLoading(true);

        const result = await adminCasesService.getCases();

        // 🔥 NORMALIZE HERE
        const payload = result?.data ?? result;

        setData(payload);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCases();
  }, []);

  return {
    data,
    loading,
    error,

    // ✅ FIXED ACCESS PATH
    summary: data?.summary,
    cases: data?.cases || [],
    lawyerPerformance: data?.lawyer_performance || [],
    topClients: data?.top_clients || [],
    courtDistribution: data?.court_distribution || [],
    caseTypeBreakdown: data?.case_type_breakdown || [],
    statusBreakdown: data?.status_breakdown || [],
    priorityBreakdown: data?.priority_breakdown || [],
    monthlyCaseIntake: data?.monthly_case_intake || [],
  };
}
