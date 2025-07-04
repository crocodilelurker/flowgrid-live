import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import DashboardClientPage from './DashBoardClient';

export default async function DashboardPage() {
  const cookieStore = await cookies();
  const jwt = cookieStore.get('jwt_token')?.value;
  if (!jwt) redirect('/auth/login'); // server fallback

  return <DashboardClientPage />;
}
