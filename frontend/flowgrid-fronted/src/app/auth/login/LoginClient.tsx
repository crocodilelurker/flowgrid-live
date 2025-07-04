'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
export default function LoginPage() {
  const [form, setForm] = useState({ username: '', password: '' });
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  try {
    console.log(form)
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(form),
    });

    const data = await res.json();

    if (data.status_code === 200) {
      console.log('Login successful. User ID:', data.user_id);
      router.push("/dashboard")
    } else {
      console.error('Login failed:', data.message);
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};


  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F5F7FA]">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-xl p-8 w-full max-w-md border border-gray-200"
      >
        <h2 className="text-2xl font-bold text-[#0066CC] mb-6 text-center">Login to FlowGrid</h2>

        <div className="mb-4">
          <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <input
            type="text"
            name="username"
            id="username"
            value={form.username}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#00A896] transition"
          />
        </div>

        <div className="mb-6">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            type="password"
            name="password"
            id="password"
            value={form.password}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#00A896] transition"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-[#14ba43] hover:bg-[#12a639] text-white font-semibold py-2 rounded-lg shadow-md transition-all duration-300"
        >
          Sign In
        </button>
      </form>
    </div>
  );
}
