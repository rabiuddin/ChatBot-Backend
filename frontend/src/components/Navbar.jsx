import React from 'react';

export default function Navbar() {
  return (
    <nav className="bg-white dark:bg-gray-900 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <span className="font-extrabold text-3xl text-gray-800 dark:text-white fixed top-4 left-5">ChatBot</span>
          </div>
        </div>
      </div>
    </nav>
  );
}

