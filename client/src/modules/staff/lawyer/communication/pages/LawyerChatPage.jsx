import { useEffect, useMemo, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { Briefcase } from 'lucide-react';

import { getApiErrorMessage } from '@/core/utils/errorMessages';
import { useMyCases } from '@/modules/staff/lawyer/cases/hooks/useLawyerCases';
import AnnouncementInboxCard from '@/modules/communications/components/AnnouncementInboxCard';
import ChatWorkspace from '@/modules/communications/components/ChatWorkspace';
import {
  useOpenCaseThread,
  useSendThreadMessage,
  useThreadMessages,
  useThreads,
} from '@/modules/communications/hooks/useCommunications';

import Button3D from '@/components/ui/Button3D';
import Card from '@/components/ui/Card';

export default function LawyerChatPage() {
  const params = useParams();
  const [searchParams] = useSearchParams();
  const routeCaseId = params.id || params.caseId || searchParams.get('case');

  const [selectedThreadId, setSelectedThreadId] = useState(null);
  const [selectedCaseId, setSelectedCaseId] = useState(routeCaseId || '');
  const [feedback, setFeedback] = useState(null);

  const casesQuery = useMyCases();
  const { data, isLoading, refetch } = useThreads();
  const openCaseThread = useOpenCaseThread();
  const messagesQuery = useThreadMessages(selectedThreadId);
  const sendMessage = useSendThreadMessage();

  const cases = casesQuery.data?.cases || [];
  const threads = data?.threads || [];

  const sortedCases = useMemo(
    () =>
      [...cases].sort((a, b) =>
        String(a.case_number).localeCompare(String(b.case_number)),
      ),
    [cases],
  );

  useEffect(() => {
    if (routeCaseId) setSelectedCaseId(routeCaseId);
  }, [routeCaseId]);

  useEffect(() => {
    if (!routeCaseId) return;
    const existingThread = threads.find(
      (thread) => String(thread.case?.id) === String(routeCaseId),
    );
    if (existingThread) setSelectedThreadId(existingThread.id);
  }, [routeCaseId, threads]);

  useEffect(() => {
    if (!selectedThreadId && threads.length) {
      setSelectedThreadId(threads[0].id);
    }
  }, [selectedThreadId, threads]);

  const handleOpenCaseThread = async (caseId = selectedCaseId) => {
    if (!caseId) {
      setFeedback({ type: 'error', text: 'Choose an assigned case first.' });
      return;
    }

    setFeedback(null);

    try {
      const response = await openCaseThread.mutateAsync(caseId);
      setSelectedThreadId(response.thread?.id);
      setFeedback({
        type: 'success',
        text: 'Case communication opened in read-only mode.',
      });
    } catch (error) {
      setFeedback({
        type: 'error',
        text: getApiErrorMessage(error, 'Could not open case communication.'),
      });
    }
  };

  const handleSendMessage = async (body) => {
    await sendMessage.mutateAsync({ threadId: selectedThreadId, body });
  };

  const sidebarExtra = (
    <div className='mt-3 rounded-xl bg-amber-50 px-3 py-2 text-xs text-amber-800 dark:bg-amber-950/50 dark:text-amber-200'>
      Lawyers can read assigned case communication only. Direct admin-staff
      chats remain replyable.
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
                Assigned case communication
              </h2>
              <p className='text-sm text-slate-500 dark:text-slate-300'>
                Open a case thread to read client-firm communication.
              </p>
            </div>
          </div>

          <div className='flex flex-col gap-3 md:flex-row'>
            <select
              value={selectedCaseId}
              onChange={(event) => setSelectedCaseId(event.target.value)}
              className='h-12 flex-1 rounded-2xl border border-border-light bg-white px-4 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-border-dark dark:bg-slate-900 dark:text-white'
            >
              <option value=''>Choose assigned case</option>
              {sortedCases.map((caseItem) => (
                <option key={caseItem.id} value={caseItem.id}>
                  {caseItem.case_number} — {caseItem.title}
                </option>
              ))}
            </select>

            <Button3D
              disabled={
                casesQuery.isLoading ||
                openCaseThread.isPending ||
                !selectedCaseId
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
        title='Lawyer Communication'
        subtitle='Read assigned case communication and reply to private admin-staff chats.'
        threads={threads}
        selectedThreadId={selectedThreadId}
        onSelectThread={(thread) => setSelectedThreadId(thread.id)}
        messages={messagesQuery.data?.messages || []}
        onSendMessage={handleSendMessage}
        isLoadingThreads={isLoading}
        isLoadingMessages={messagesQuery.isLoading}
        isSending={sendMessage.isPending}
        onRefresh={refetch}
        sidebarExtra={sidebarExtra}
        readOnlyMessage='Assigned lawyers can read client-firm case communication but replies are handled by the secretary or admin.'
        emptyThreadMessage='No accessible communication threads yet.'
      />
    </div>
  );
}
