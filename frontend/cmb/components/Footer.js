'use client';

import { useRouter } from 'next/router';
import { ChatBubbleLeftRightIcon, HomeIcon, PhotoIcon, CloudArrowUpIcon } from '@heroicons/react/24/outline';

const Footer = () => {
  const router = useRouter();

  const navigation = [
    { name: 'Home', path: '/', icon: HomeIcon },
    { name: 'Gallery', path: '/gallery', icon: PhotoIcon },
    { name: 'Batch Upload', path: '/batch-uploader', icon: CloudArrowUpIcon },
    { name: 'Chatbot', path: '/chatbot', icon: ChatBubbleLeftRightIcon },
  ];

  const handleNavigation = (path) => {
    router.push(path);
  };

  return (
    <footer className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Memory Bot</h3>
            <p className="text-gray-300">
              Empowering conversations through intelligent memory management.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              {navigation.map((item) => (
                <li key={item.name}>
                  <button
                    onClick={() => handleNavigation(item.path)}
                    className="text-gray-300 hover:text-white transition duration-300"
                  >
                    {item.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <div className="text-gray-300 space-y-2">
              <p>Email: contact@memorybot.com</p>
              <p>Phone: (555) 123-4567</p>
              <p>Address: 123 AI Street, Tech City</p>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-indigo-600 mt-8 pt-8 text-center text-gray-300">
          <p>© {new Date().getFullYear()} Memory Bot. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;