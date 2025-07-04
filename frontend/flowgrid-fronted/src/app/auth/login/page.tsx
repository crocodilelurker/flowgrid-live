import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import LoginPage from './LoginClient'; // rename your existing component

export default async function Login() {
  const cookieStore = await cookies();
  const jwt = cookieStore.get('jwt_token')?.value;
  if (jwt) {
    // Token exists → redirect away from login page
    redirect('/dashboard');
  }

  return <LoginPage />;
}
