'use client';

import Link from 'next/link';

 function Navbar() {
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