'use client';

import Link from 'next/link';

type NavbarProps = {
  isLoggedIn?: boolean;
  balance?: number;
};

 function Navbar({ 
  isLoggedIn = false, 
  balance = 0 
}: NavbarProps) {
  return (
    <nav className="bg-gray-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex-shrink-0">
            <Link href="/" className="flex items-center">
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                FlowGrid
              </span>
            </Link>
          </div>

          {/* Primary Nav */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <NavLink href="/betting">Betting</NavLink>
              <NavLink href="/trading">Trading</NavLink>
              <NavLink href="/nfts">NFTs</NavLink>
            </div>
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-4">
            {/* User Balance */}
            {isLoggedIn && (
              <div className="hidden md:flex items-center space-x-1 bg-gray-800 px-3 py-1 rounded-md">
                <span className="text-sm font-medium">Balance:</span>
                <span className="font-bold text-blue-300">{balance} FGC</span>
              </div>
            )}

            {/* Auth Buttons */}
            {isLoggedIn ? (
              <Link
                href="/logout"
                className="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 rounded-md transition"
              >
                Sign Out
              </Link>
            ) : (
              <div className="flex space-x-2">
                <Link
                  href="/login"
                  className="px-4 py-2 text-sm bg-gray-700 hover:bg-gray-600 rounded-md transition"
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 rounded-md transition"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-800 transition"
    >
      {children}
    </Link>
  );
}
export default Navbar;