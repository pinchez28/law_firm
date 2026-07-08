import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';

import ChatWorkspace from '@/modules/communications/components/ChatWorkspace';
import {
  useAdminThreads,
  useSendThreadMessage,
  useThreadMessages,
} from '@/modules/communications/hooks/useCommunications';

import Card from '@/components/ui/Card';

export default function AdminClientCommunicationPage() {
  const { id } = useParams();
  const [selectedThreadId, setSelectedThreadId] = useState(null);

  const { data, isLoading, refetch } = useAdminThreads({
    thread_type: 'CASE_CLIENT',
  });
  const messagesQuery = useThreadMessages(selectedThreadId);
  const sendMessage = useSendThreadMessage();

  const threads = useMemo(() => {
    const allThreads = data?.threads || [];
    return allThreads.filter(
      (thread) => String(thread.case?.client?.id) === String(id),
    );
  }, [data?.threads, id]);

  useEffect(() => {
    if (!selectedThreadId && threads.length) {
      setSelectedThreadId(threads[0].id);
      return;
    }

    if (
      selectedThreadId &&
      !threads.some((thread) => String(thread.id) === String(selectedThreadId))
    ) {
      setSelectedThreadId(threads[0]?.id || null);
    }
  }, [selectedThreadId, threads]);

  const handleSendMessage = async (body) => {
    await sendMessage.mutateAsync({ threadId: selectedThreadId, body });
  };

  return (
    <div className='space-y-6 p-4 md:p-6 animate-fadeIn'>
      {!threads.length && !isLoading && (
        <Card className='p-5 text-sm text-slate-500 dark:text-slate-300'>
          No case communication threads exist for this client yet. Threads are
          created per case when the client or firm opens case communication.
        </Card>
      )}

      <ChatWorkspace
        title='Client Case Communication'
        subtitle='Admin view of all case-specific communication threads for this client.'
        threads={threads}
        selectedThreadId={selectedThreadId}
        onSelectThread={(thread) => setSelectedThreadId(thread.id)}
        messages={messagesQuery.data?.messages || []}
        onSendMessage={handleSendMessage}
        isLoadingThreads={isLoading}
        isLoadingMessages={messagesQuery.isLoading}
        isSending={sendMessage.isPending}
        onRefresh={refetch}
        emptyThreadMessage='No communication threads for this client.'
      />
    </div>
  );
}
