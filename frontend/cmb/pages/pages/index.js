import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from "../components/Navbar";
import Footer from '../components/Footer';

const images = [
  '/images/i1.jpg',
  '/images/i2.jpg',
  '/images/i3.jpg'
];


const features = [
  {
    title: "AI-Powered Gallery",
    description: "Transform and manage your images with our state-of-the-art AI processing system. Experience intelligent organization and enhancement capabilities.",
    icon: () => (
      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
    href: "/gallery",
    button: "Explore Gallery",
    gradient: "from-blue-600 via-blue-500 to-indigo-600",
    hoverGradient: "hover:from-blue-700 hover:via-blue-600 hover:to-indigo-700",
    shadowColor: "shadow-blue-500/30"
  },
  {
    title: "Smart Upload Studio",
    description: "Upload and process multiple images simultaneously with our intelligent batch processing system. Save time with automated optimization.",
    icon: () => (
      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
    ),
    href: "/batch-uploader",
    button: "Start Uploading",
    gradient: "from-emerald-600 via-emerald-500 to-teal-600",
    hoverGradient: "hover:from-emerald-700 hover:via-emerald-600 hover:to-teal-700",
    shadowColor: "shadow-emerald-500/30"
  },
  {
    title: "AI Assistant",
    description: "Engage with our advanced AI chatbot for real-time assistance and insights. Get intelligent responses powered by cutting-edge language models.",
    icon: () => (
      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    ),
    href: "/chatbot",
    button: "Chat Now",
    gradient: "from-violet-600 via-purple-500 to-fuchsia-600",
    hoverGradient: "hover:from-violet-700 hover:via-purple-600 hover:to-fuchsia-700",
    shadowColor: "shadow-purple-500/30"
  }
];


const useInView = (ref, options = {}) => {
  const [isInView, setIsInView] = useState(false);


  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      setIsInView(entry.isIntersecting);
    }, options);


    if (ref.current) {
      observer.observe(ref.current);
    }


    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [ref, options]);


  return isInView;
};


const HomePage = () => {
  const [currentImage, setCurrentImage] = useState(0);
  const [scrollY, setScrollY] = useState(0);
 
  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);


  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);


  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-black to-gray-900 text-gray-100 font-sans">
      {/* Hero Section */}
      <Navbar />
      
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentImage}
            initial={{ opacity: 0, scale: 1.1 }}
            animate={{ opacity: 0.7, scale: 1 }}
            exit={{ opacity: 0, scale: 1.1 }}
            transition={{ duration: 1.5 }}
            className="absolute inset-0 w-full h-full"
            style={{
              backgroundImage: `url(${images[currentImage]})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              filter: 'brightness(0.4)'
            }}
          />
        </AnimatePresence>
       
        <motion.div
          className="relative z-10 text-center px-6 max-w-5xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
        >
          <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mb-6">
            Next-Gen AI Innovation
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed">
            Experience the future of artificial intelligence with our cutting-edge platform.
            Transform your workflow with powerful AI-driven tools and insights.
          </p>
          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
          >
            <motion.a
              href="/gallery"
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl font-semibold text-lg shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 transition-all duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Get Started
            </motion.a>
            <motion.a
              href="/demo"
              className="px-8 py-4 bg-gradient-to-r from-gray-800 to-gray-900 rounded-xl font-semibold text-lg border border-gray-700 hover:border-gray-500 transition-all duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Watch Demo
            </motion.a>
          </motion.div>
        </motion.div>


        <motion.div
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
          animate={{
            y: [0, 10, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          <svg
            className="w-8 h-8 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </motion.div>
      </section>


      {/* Features Section */}
      <section className="py-24 px-6 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Powerful Features
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Discover our suite of advanced AI tools designed to transform your workflow
              and enhance productivity.
            </p>
          </motion.div>


          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard key={index} feature={feature} index={index} />
            ))}
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
};


const FeatureCard = ({ feature, index }) => {
  const cardRef = useRef(null);
  const isInView = useInView(cardRef, { threshold: 0.2 });


  return (
    <motion.div
      ref={cardRef}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.8, delay: index * 0.2 }}
      className="relative group"
    >
      <div className="relative z-10 h-full bg-gray-800 bg-opacity-50 backdrop-blur-xl rounded-2xl p-8 border border-gray-700 transition-all duration-300 hover:border-gray-500">
        <div className={`w-16 h-16 rounded-xl mb-6 flex items-center justify-center bg-gradient-to-r ${feature.gradient}`}>
          <feature.icon />
        </div>
       
        <h3 className="text-2xl font-semibold mb-4">{feature.title}</h3>
        <p className="text-gray-400 mb-6">{feature.description}</p>
       
        <motion.a
          href={feature.href}
          className={`block w-full py-3 px-6 rounded-xl bg-gradient-to-r ${feature.gradient} ${feature.hoverGradient} ${feature.shadowColor} transition-all duration-300 text-center`}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {feature.button}
        </motion.a>
      </div>
     
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 blur-xl transition-all duration-500" />
    </motion.div>
  );
};


export default HomePage;

