import { useMemo, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { Briefcase, Inbox } from 'lucide-react';

import { getApiErrorMessage } from '@/core/utils/errorMessages';
import useSecretaryCases from '@/modules/staff/secretary/cases/hooks/useSecretaryCases';
import AnnouncementInboxCard from '@/modules/communications/components/AnnouncementInboxCard';
import ChatWorkspace from '@/modules/communications/components/ChatWorkspace';
import {
  useOpenCaseThread,
  useSecretaryCaseThreads,
  useSendThreadMessage,
  useThreadMessages,
} from '@/modules/communications/hooks/useCommunications';

import Button3D from '@/components/ui/Button3D';
import Card from '@/components/ui/Card';

export default function SecretaryChat() {
  const params = useParams();
  const [searchParams] = useSearchParams();
  const routeCaseId = params.id || params.caseId || searchParams.get('case');

  const [selectedCaseId, setSelectedCaseId] = useState(routeCaseId || '');
  const [feedback, setFeedback] = useState(null);

  const { cases, loading: casesLoading } = useSecretaryCases();
  const { data, isLoading, refetch } = useSecretaryCaseThreads();
  const openCaseThread = useOpenCaseThread();

  // ✅ Fix Warnings 4 & 5 — wrap threads in useMemo for stable reference
  const threads = useMemo(() => data?.threads || [], [data?.threads]);

  const sortedCases = useMemo(
    () =>
      [...(cases || [])].sort((a, b) =>
        String(a.case_number).localeCompare(String(b.case_number)),
      ),
    [cases],
  );

  // ✅ Fix Errors 1, 2 & 3 — derive selectedThreadId without useEffect
  // Priority: match thread by routeCaseId → first thread → null
  const defaultThreadId = useMemo(() => {
    if (!threads.length) return null;

    // If a routeCaseId exists, find its matching thread first
    if (routeCaseId) {
      const matchedThread = threads.find(
        (thread) => String(thread.case?.id) === String(routeCaseId),
      );
      if (matchedThread) return matchedThread.id;
    }

    // Fallback to first thread
    return threads[0].id;
  }, [routeCaseId, threads]);

  // User can still manually change thread via sidebar or after opening a thread
  const [selectedThreadId, setSelectedThreadId] = useState(defaultThreadId);

  // ✅ Ensure selectedThreadId is always valid within current threads list
  const resolvedThreadId = useMemo(() => {
    if (!threads.length) return null;
    const stillExists = threads.some(
      (thread) => String(thread.id) === String(selectedThreadId),
    );
    return stillExists ? selectedThreadId : (threads[0]?.id ?? null);
  }, [threads, selectedThreadId]);

  const messagesQuery = useThreadMessages(resolvedThreadId);
  const sendMessage = useSendThreadMessage();

  // ✅ All three useEffect blocks removed — no more cascading renders

  const handleOpenCaseThread = async (caseId = selectedCaseId) => {
    if (!caseId) {
      setFeedback({ type: 'error', text: 'Choose a case first.' });
      return;
    }

    setFeedback(null);

    try {
      const response = await openCaseThread.mutateAsync(caseId);
      setSelectedThreadId(response.thread?.id);
      setFeedback({ type: 'success', text: 'Case communication opened.' });
    } catch (error) {
      setFeedback({
        type: 'error',
        text: getApiErrorMessage(error, 'Could not open case communication.'),
      });
    }
  };

  const handleSendMessage = async (body) => {
    await sendMessage.mutateAsync({ threadId: resolvedThreadId, body });
  };

  const sidebarExtra = (
    <div className='mt-3 rounded-xl bg-blue-50 px-3 py-2 text-xs text-blue-800 dark:bg-blue-950/50 dark:text-blue-200'>
      Secretary access: all client-case communication threads.
    </div>
  );

  return (
    <div className='space-y-6 p-4 md:p-6 animate-fadeIn'>
      <div className='grid gap-4 xl:grid-cols-[420px_1fr]'>
        <AnnouncementInboxCard compact />

        <Card className='p-5'>
          <div className='mb-4 flex items-center gap-2'>
            <Briefcase size={20} />
            <div>
              <h2 className='font-bold text-slate-900 dark:text-white'>
                Open case communication
              </h2>
              <p className='text-sm text-slate-500 dark:text-slate-300'>
                Create or open the client communication thread for a case.
              </p>
            </div>
          </div>

          <div className='flex flex-col gap-3 md:flex-row'>
            <select
              value={selectedCaseId}
              onChange={(event) => setSelectedCaseId(event.target.value)}
              className='h-12 flex-1 rounded-2xl border border-border-light bg-white px-4 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-border-dark dark:bg-slate-900 dark:text-white'
            >
              <option value=''>Choose case</option>
              {sortedCases.map((caseItem) => (
                <option key={caseItem.id} value={caseItem.id}>
                  {caseItem.case_number} — {caseItem.title}
                </option>
              ))}
            </select>

            <Button3D
              disabled={
                casesLoading || openCaseThread.isPending || !selectedCaseId
              }
              onClick={() => handleOpenCaseThread()}
            >
              {openCaseThread.isPending ? 'Opening...' : 'Open thread'}
            </Button3D>
          </div>

          {feedback && (
            <div
              className={`mt-4 rounded-xl px-4 py-3 text-sm ${
                feedback.type === 'success'
                  ? 'bg-green-50 text-green-700 dark:bg-green-950/40 dark:text-green-200'
                  : 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-200'
              }`}
            >
              {feedback.text}
            </div>
          )}
        </Card>
      </div>

      <ChatWorkspace
        title='Secretary Client Communication'
        subtitle='Manage all client-firm communication threads per case.'
        threads={threads}
        selectedThreadId={resolvedThreadId}
        onSelectThread={(thread) => setSelectedThreadId(thread.id)}
        messages={messagesQuery.data?.messages || []}
        onSendMessage={handleSendMessage}
        isLoadingThreads={isLoading}
        isLoadingMessages={messagesQuery.isLoading}
        isSending={sendMessage.isPending}
        onRefresh={refetch}
        sidebarExtra={sidebarExtra}
        emptyThreadMessage='No client case communication threads yet.'
      />

      {!threads.length && !isLoading && (
        <Card className='p-5 text-sm text-slate-500 dark:text-slate-300'>
          <div className='flex items-center gap-2 font-semibold text-slate-800 dark:text-white'>
            <Inbox size={18} />
            Tip
          </div>
          <p className='mt-2'>
            Select a case above and open its communication thread to begin
            client-firm communication.
          </p>
        </Card>
      )}
    </div>
  );
}
