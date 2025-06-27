import './globals.css';
import Navbar from '@/components/Navbar';
export default function Home() {
    const isLoggedIn = true;
    const balance = 1450;
  return (
    <div>
      <Navbar isLoggedIn={true} balance={1450} />
    </div>
    //now simulating a homepage if user is not logged in and another if user is logged in
    
  );
}
