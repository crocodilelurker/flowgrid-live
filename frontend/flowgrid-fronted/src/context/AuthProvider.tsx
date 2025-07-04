'use client';

import { createContext, useEffect, useState } from 'react';

type AuthData = {
  user_id: string;
  username: string;
};

const AuthContext = createContext<AuthData | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [auth, setAuth] = useState<AuthData | null>(null);

  useEffect(() => {
    const verify = async () => {
      try {
        const res = await fetch('http://localhost:8000/auth/verify-token', {
          method: 'GET',
          credentials: 'include',
        });

        const data = await res.json();

        if (data.status_code === 200) {
          setAuth({ user_id: data.user_id, username: data.username });
        } else {
          setAuth(null);
        }
      } catch (error) {
        console.error('Token verification failed:', error);
        setAuth(null);
      }
    };

    verify();
  }, []);

  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export default AuthContext;
