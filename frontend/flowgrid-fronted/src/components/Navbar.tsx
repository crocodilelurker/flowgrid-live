'use client';

import Link from 'next/link';

function Navbar() {
  return (
    <nav className="bg-[#F5F7FA] text-[#0066CC] shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <Link
            href="/"
            className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-[#00A896] to-[#14ba43]"
          >
            FlowGrid
          </Link>

          {/* Nav Links */}
          <div className="flex items-center space-x-6">
            <NavLink href="/auth/login">Login</NavLink>
            <CTAButton href="/auth/signup">Get Started</CTAButton>
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
      className="text-[#0066CC] hover:text-[#00A896] transition-colors duration-200 font-medium text-sm"
    >
      {children}
    </Link>
  );
}

function CTAButton({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className="bg-[#14ba43] hover:bg-[#12a639] text-white px-5 py-2 rounded-xl font-semibold text-sm shadow-md transition-all duration-300"
    >
      {children}
    </Link>
  );
}

export default Navbar;
