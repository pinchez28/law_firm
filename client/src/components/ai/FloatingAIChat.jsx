import { useState, useRef, useEffect } from 'react';

export default function FloatingAIChat() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const chatRef = useRef(null);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (chatRef.current && !chatRef.current.contains(event.target)) {
        setOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div
      ref={chatRef}
      className='fixed bottom-6 right-6 z-[9999] flex flex-col items-end'
    >
      {/* Chat Panel */}
      {open && (
        <div
          className='
            w-[340px] sm:w-[380px]
            h-[420px]
            mb-3
            rounded-2xl
            shadow-strong
            border
            border-border-light dark:border-border-dark
            bg-surface-light dark:bg-surface-dark
            flex flex-col
            animate-fadeIn
            overflow-hidden
          '
        >
          {/* Header */}
          <div className='px-4 py-3 border-b border-border-light dark:border-border-dark'>
            <p className='text-sm font-semibold text-text-primary-light dark:text-text-primary-dark'>
              Legal Assistant
            </p>
            <p className='text-xs text-text-muted-light dark:text-text-muted-dark'>
              Ask any legal or firm-related question
            </p>
          </div>

          {/* Messages */}
          <div className='flex-1 p-3 overflow-y-auto'>
            <div className='text-sm text-text-muted-light dark:text-text-muted-dark'>
              Start by typing your question...
            </div>
          </div>

          {/* Input */}
          <div className='p-3 border-t border-border-light dark:border-border-dark'>
            <div className='flex items-center gap-2'>
              <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder='Ask your legal question...'
                className='
                  flex-1
                  px-3 py-2
                  rounded-md
                  bg-background-light dark:bg-background-dark
                  border border-border-light dark:border-border-dark
                  text-text-primary-light dark:text-text-primary-dark
                  placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark
                  focus:outline-none focus:ring-2 focus:ring-success
                '
              />

              <button
                className='
                  px-3 py-2
                  rounded-md
                  bg-success
                  text-white
                  font-semibold
                  hover:opacity-90
                  transition
                '
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating Button (Dark mode optimized) */}
      <button
        onClick={() => setOpen(!open)}
        className='
          px-6
          h-12
          rounded-md
          bg-white
          dark:bg-emerald-500
          text-gray-900
          font-extrabold
          shadow-strong
          hover:scale-105
          transition
          flex items-center justify-center
        '
      >
        {open ? '✕' : 'Have any Firm related or Legal Question?'}
      </button>
    </div>
  );
}
