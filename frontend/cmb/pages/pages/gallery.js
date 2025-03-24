'use client';

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ChevronLeftIcon, 
  ChevronRightIcon, 
  XMarkIcon,
  InformationCircleIcon,
  TagIcon,
  ArrowPathIcon,
  MagnifyingGlassPlusIcon,
  MagnifyingGlassMinusIcon
} from "@heroicons/react/24/outline";
import Navbar from "../components/Navbar";
import Footer from '../components/Footer';

const Gallery = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(1);

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4 }
    }
  };

  useEffect(() => {
    const fetchImages = async () => {
      try {
        setIsLoading(true);
        const response = await fetch("/api/images");
        const data = await response.json();
        setImages(data.images || []);
      } catch (error) {
        console.error("Error fetching images:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchImages();
  }, []);

  const handleImageClick = (image, index) => {
    setSelectedImage(image);
    setCurrentIndex(index);
    setZoomLevel(1);
  };

  const navigate = (direction) => {
    const newIndex = direction === 'next'
      ? (currentIndex + 1) % images.length
      : (currentIndex - 1 + images.length) % images.length;
    
    setSelectedImage(images[newIndex]);
    setCurrentIndex(newIndex);
    setZoomLevel(1);
  };

  const closeModal = () => {
    setSelectedImage(null);
    setZoomLevel(1);
  };

  // Zoom functions
  const zoomIn = () => {
    setZoomLevel(prev => Math.min(prev + 0.2, 3));
  };

  const zoomOut = () => {
    setZoomLevel(prev => Math.max(prev - 0.2, 0.5));
  };

  const handleWheel = (e) => {
    e.preventDefault();
    if (e.deltaY < 0) {
      zoomIn();
    } else {
      zoomOut();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 py-12">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="space-y-8"
        >
          <motion.div 
            variants={itemVariants}
            className="text-center space-y-4"
          >
            <h1 className="text-5xl font-bold text-gray-800 font-serif">
              Image Gallery
            </h1>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Explore our curated collection of stunning images
            </p>
          </motion.div>

          {isLoading && (
            <div className="flex justify-center items-center h-64">
              <ArrowPathIcon className="w-8 h-8 text-blue-500 animate-spin" />
            </div>
          )}

          <motion.div 
            className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6"
            variants={containerVariants}
          >
            {images.map((image, idx) => (
              <motion.div
                key={idx}
                variants={itemVariants}
                className="relative group aspect-square overflow-hidden rounded-xl shadow-lg"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleImageClick(image, idx)}
              >
                <motion.img
                  src={image.src}
                  alt={`Gallery item ${idx + 1}`}
                  
                  className="w-full h-full object-cover cursor-pointer transform transition-all duration-300"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                  <span className="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    View
                  </span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        <AnimatePresence>
          {selectedImage && (
            <motion.div
              className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center p-4 z-[1000]"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={closeModal}
            >
              <motion.div
                className="relative bg-white rounded-2xl shadow-2xl max-w-7xl w-full overflow-hidden"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={e => e.stopPropagation()}
              >
                <div className="flex flex-col md:flex-row">
                  {/* Image Container with Zoom */}
                  <div 
                    className="w-full md:w-2/3 bg-gray-900 relative overflow-hidden"
                    onWheel={handleWheel} // Mouse wheel zoom
                  >
                    <motion.img
                      src={selectedImage.src}
                      alt="Selected"
                      className="w-full h-[70vh] object-contain cursor-grab"
                      style={{ scale: zoomLevel }} // Apply zoom level
                      animate={{ scale: zoomLevel }}
                      transition={{ duration: 0.2 }}
                    />
                    
                    {/* Navigation Buttons */}
                    <button
                      onClick={() => navigate('prev')}
                      className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/90 p-2 rounded-full hover:bg-white transition-all duration-300"
                    >
                      <ChevronLeftIcon className="w-6 h-6 text-gray-800" />
                    </button>
                    <button
                      onClick={() => navigate('next')}
                      className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/90 p-2 rounded-full hover:bg-white transition-all duration-300"
                    >
                      <ChevronRightIcon className="w-6 h-6 text-gray-800" />
                    </button>

                    {/* Zoom Controls */}
                    <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
                      <button
                        onClick={zoomOut}
                        className="bg-white/90 p-2 rounded-full hover:bg-white transition-all duration-300"
                        disabled={zoomLevel <= 0.5}
                      >
                        <MagnifyingGlassMinusIcon className="w-6 h-6 text-gray-800" />
                      </button>
                      <button
                        onClick={zoomIn}
                        className="bg-white/90 p-2 rounded-full hover:bg-white transition-all duration-300"
                        disabled={zoomLevel >= 3}
                      >
                        <MagnifyingGlassPlusIcon className="w-6 h-6 text-gray-800" />
                      </button>
                    </div>
                  </div>

                  {/* Info Panel */}
                  <div className="w-full md:w-1/3 p-6 bg-white">
                    <div className="h-full flex flex-col">
                      <div className="flex items-center space-x-2 mb-6">
                        <InformationCircleIcon className="w-6 h-6 text-blue-500" />
                        <h2 className="text-2xl font-semibold text-gray-800">
                          Details
                        </h2>
                      </div>
                      <p className="text-gray-600 mb-6 flex-grow">
                        {selectedImage.description || "No description available."}
                      </p>
                      <div className="space-y-4">
                        <div className="flex items-center space-x-2">
                          <TagIcon className="w-5 h-5 text-blue-500" />
                          <h3 className="text-lg font-medium text-gray-800">
                            Tags
                          </h3>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {selectedImage.tags && selectedImage.tags.length > 0 ? (
                            selectedImage.tags.map((tag, idx) => (
                              <motion.span
                                key={idx}
                                className="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-sm font-medium"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                              >
                                #{tag}
                              </motion.span>
                            ))
                          ) : (
                            <p>No tags available</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Close Button */}
                <button
                  onClick={closeModal}
                  className="absolute top-4 right-4 bg-white/90 p-2 rounded-full hover:bg-white transition-all duration-300"
                >
                  <XMarkIcon className="w-6 h-6 text-gray-800" />
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <Footer />
    </div>
  );
};


export async function getStaticProps() {
  try {
    const res = await fetch("http://localhost:8000/api/images"); // Adjust URL as needed
    const data = await res.json();
    return { props: { images: data.images || [] } };
  } catch (error) {
    console.error("Error fetching images:", error);
    return { props: { images: [] } };
  }
}

export default Gallery;
