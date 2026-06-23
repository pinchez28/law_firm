import { useEffect, useMemo, useRef, useState } from 'react';

import ThemeContext from '@/core/store/ThemeContext';

const ThemeProvider = ({ children, user, role }) => {
  const storageKey = useMemo(() => {
    const uniqueUserId =
      user?.user_id || user?.id || user?._id || user?.email || 'guest';

    return `theme-${role || 'public'}-${uniqueUserId}`;
  }, [role, user?.user_id, user?.id, user?._id, user?.email]);

  /*
    Prevent unnecessary sync loops
  */
  const previousStorageKey = useRef(storageKey);

  /*
    Initialize instantly from localStorage
    to avoid flash/flicker
  */
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem(storageKey) || 'light';
  });

  /*
    Only update theme if actual user changes
  */
  useEffect(() => {
    if (previousStorageKey.current !== storageKey) {
      previousStorageKey.current = storageKey;

      const savedTheme = localStorage.getItem(storageKey) || 'light';

      setTheme(savedTheme);
    }
  }, [storageKey]);

  /*
    Apply theme to DOM + persist
  */
  useEffect(() => {
    const root = document.documentElement;

    root.classList.toggle('dark', theme === 'dark');

    localStorage.setItem(storageKey, theme);
  }, [theme, storageKey]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        setTheme,
        toggleTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
