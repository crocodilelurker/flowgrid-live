'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

export default function DashboardClientPage() {
  const auth = useAuth();
  const router = useRouter();
   useEffect(() => {
    console.log('Auth context:', auth);
  }, [auth,router]);

  if (!auth) return null; // Optionally show a loading spinner
  
  return (
    <div>
      <h1>Welcome, {auth.username}</h1>
      <p>Your user ID is {auth.user_id}</p>
    </div>
  );
}