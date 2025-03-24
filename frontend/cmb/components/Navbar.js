'use client';

import { useState } from 'react';
import { useRouter } from 'next/router';
import { Bars3Icon, XMarkIcon, ChatBubbleLeftRightIcon, HomeIcon, PhotoIcon, CloudArrowUpIcon } from '@heroicons/react/24/outline';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  const handleNavigation = (path) => {
    router.push(path);
    setIsOpen(false);
  };

  const navigation = [
    { name: 'Home', path: '/', icon: HomeIcon },
    { name: 'Gallery', path: '/gallery', icon: PhotoIcon },
    { name: 'Image Upload', path: '/batch-uploader', icon: CloudArrowUpIcon },
    { name: 'Chatbot', path: '/chatbot', icon: ChatBubbleLeftRightIcon },
  ];

  return (
    <nav className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-lg fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-12 items-center">
          {/* Logo */}
          <h1 
            onClick={() => handleNavigation('/')}
            className="text-2xl font-extrabold tracking-wide cursor-pointer hover:text-gray-200 transition duration-300"
          >
            
            Conversational Memory Bot
          </h1>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <button
                key={item.name}
                onClick={() => handleNavigation(item.path)}
                className="flex items-center space-x-2 text-white hover:text-gray-200 transition duration-300 group"
              >
                <item.icon className="h-5 w-5" />
                <span className="relative after:block after:h-0.5 after:w-0 after:bg-white after:transition-all after:duration-300 group-hover:after:w-full">
                  {item.name}
                </span>
              </button>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden rounded-md p-2 hover:bg-indigo-700 transition duration-300"
          >
            {isOpen ? (
              <XMarkIcon className="h-6 w-6" />
            ) : (
              <Bars3Icon className="h-6 w-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden absolute top-16 left-0 right-0 bg-indigo-800">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navigation.map((item) => (
              <button
                key={item.name}
                onClick={() => handleNavigation(item.path)}
                className="flex items-center w-full px-3 py-2 text-white hover:bg-indigo-700 transition duration-300"
              >
                <item.icon className="h-5 w-5 mr-3" />
                {item.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;