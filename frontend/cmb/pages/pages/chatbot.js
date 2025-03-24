"use client";

import { useState, useEffect, useRef } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { PaperAirplaneIcon, PhotoIcon, XMarkIcon, PhotoIcon as GalleryIcon, DocumentIcon } from "@heroicons/react/24/outline";
import SubpageLayout from "../components/SubpageLayout";
import { useRouter } from "next/router";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [inputImages, setInputImages] = useState([]);
  const [showUploadOptions, setShowUploadOptions] = useState(false);
  const [showGalleryModal, setShowGalleryModal] = useState(false);
  const [galleryImages, setGalleryImages] = useState([]);
  const [selectedGalleryImages, setSelectedGalleryImages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [enlargedImage, setEnlargedImage] = useState(null);
  const [showMultiImageWarning, setShowMultiImageWarning] = useState(false);
  const messagesEndRef = useRef(null);
  const router = useRouter();

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.2 } },
  };
  const messageVariants = {
    hidden: { opacity: 0, y: 20, scale: 0.95 },
    visible: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.3, ease: "easeOut" } },
    exit: { opacity: 0, y: -20, transition: { duration: 0.2 } },
  };
  const headerVariants = {
    hidden: { opacity: 0, y: -30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } },
  };
  const inputVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: 0.3, ease: "easeOut" } },
  };
  const modalVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.3, ease: "easeOut" } },
    exit: { opacity: 0, scale: 0.9, transition: { duration: 0.2 } },
  };
  const optionVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.2, ease: "easeOut" } },
    exit: { opacity: 0, x: -20, transition: { duration: 0.15 } },
  };

  // Scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handle image drop from file
  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 1) {
      setShowMultiImageWarning(true);
      return;
    }
    const newImage = Object.assign(acceptedFiles[0], { preview: URL.createObjectURL(acceptedFiles[0]) });
    setInputImages([newImage]);
    setShowUploadOptions(false);
    console.log("Dropped image:", newImage);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  // Fetch gallery images when modal opens
  useEffect(() => {
    if (showGalleryModal) {
      const fetchGalleryImages = async () => {
        try {
          const response = await fetch("/api/images");
          if (!response.ok) throw new Error("Failed to fetch gallery images");
          const data = await response.json();
          setGalleryImages(data.images || []);
        } catch (error) {
          console.error("Error fetching gallery images:", error);
          setGalleryImages([]);
        }
      };
      fetchGalleryImages();
    }
  }, [showGalleryModal]);

  // Handle gallery image selection (limit to one)
  const toggleGalleryImageSelection = (image) => {
    setSelectedGalleryImages((prev) =>
      prev.some((img) => img.src === image.src)
        ? []
        : [image]
    );
  };

  // Handle upload from gallery
  const handleGalleryUpload = () => {
    if (selectedGalleryImages.length > 1) {
      setShowMultiImageWarning(true);
      return;
    }
    const newImage = { preview: selectedGalleryImages[0].src };
    setInputImages([newImage]);
    setShowGalleryModal(false);
    setSelectedGalleryImages([]);
    setShowUploadOptions(false);
    console.log("Gallery image added:", newImage);
  };

  // Remove an image from input
  const removeImage = (index) => {
    setInputImages((prev) => prev.filter((_, i) => i !== index));
  };

  // Send query to backend
  const sendToBackend = async (text, images) => {
    const formData = new FormData();
    if (text) formData.append("text", text);
    console.log("Frontend text:", text);
    console.log("Frontend images count:", images.length);
    console.log("Frontend images details:", images);

    const imagePaths = images.map((image) => {
      if (image instanceof File) {
        formData.append("imageFiles", image);
        return null;
      } else if (image.preview) {
        return image.preview;
      }
      return null;
    }).filter(Boolean);

    if (imagePaths.length > 0) {
      formData.append("imagePaths", JSON.stringify(imagePaths));
      console.log("Added imagePaths to formData:", imagePaths);
    }
    console.log("FormData contents:");
    for (const [key, value] of formData.entries()) {
      console.log(`${key}:`, value instanceof File ? `File(${value.name})` : value);
    }

    try {
      console.log("Sending to /api/chatbot with method:", "POST");
      const response = await fetch("/api/chatbot", {
        method: "POST",
        body: formData,
      });
      console.log("Response status:", response.status);

      if (!response.ok) throw new Error(`Backend request failed: ${response.statusText}`);
      const data = await response.json();
      console.log("Received data from backend:", data);

      return {
        text: data.text || "No response text from backend",
        images: data.images || [],
        isBot: true,
      };
    } catch (error) {
      console.error("Error sending to backend:", error);
      return {
        text: "Sorry, something went wrong on our end!",
        images: [],
        isBot: true,
      };
    }
  };

  // Handle sending a message with backend integration
  const handleSend = async () => {
    if (!inputText.trim() && inputImages.length === 0) return;

    const userMessage = { text: inputText, images: inputImages, isBot: false };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setInputImages([]);
    setIsLoading(true);

    const botResponse = await sendToBackend(inputText, inputImages);
    console.log("Bot response prepared:", botResponse);
    setMessages((prev) => [...prev, botResponse]);
    setIsLoading(false);
  };

  // Handle image click to enlarge
  const handleImageClick = (img) => {
    setEnlargedImage(img);
  };

  // Close enlarged image modal
  const closeEnlargedImage = () => {
    setEnlargedImage(null);
  };

  // Close multiple image warning modal
  const closeMultiImageWarning = () => {
    setShowMultiImageWarning(false);
  };

  return (
    <SubpageLayout>
      <motion.div
        className="min-h-screen bg-gradient-to-br from-gray-50 to-indigo-100 flex flex-col"
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-12 flex flex-col">
          {/* Fixed Chat Header */}
          <motion.div
            className="fixed top-0 left-0 right-0 max-w-4xl mx-auto px-4 pt-12 z-20 bg-gradient-to-br from-gray-50 to-indigo-100"
            variants={headerVariants}
          >
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-800 font-serif tracking-tight">
                Chatbot Assistant
              </h1>
              <p className="text-gray-500 mt-2 text-lg font-light">
                Engage in conversations and share images effortlessly
              </p>
            </div>
          </motion.div>

          {/* Messages Container Adjusted for Fixed Header */}
          <motion.div
            className="flex-1 overflow-y-auto bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-6 border border-gray-200 mt-32" // Added mt-32 to offset header height
            variants={containerVariants}
            style={{ paddingBottom: "8rem" }}
          >
            <AnimatePresence>
              {messages.map((msg, index) => (
                <motion.div
                  key={index}
                  variants={messageVariants}
                  initial="hidden"
                  animate="visible"
                  exit="exit"
                  className={`flex ${msg.isBot ? "justify-start" : "justify-end"} mb-4`}
                >
                  <motion.div
                    className={`max-w-[70%] p-4 rounded-xl shadow-md ${
                      msg.isBot
                        ? "bg-gradient-to-r from-blue-100 to-indigo-100 text-gray-800"
                        : "bg-gradient-to-r from-blue-500 to-indigo-500 text-white"
                    }`}
                    whileHover={{ scale: 1.02, transition: { duration: 0.2 } }}
                  >
                    {msg.text && <p className="mb-2 text-sm">{msg.text}</p>}
                    {msg.images && msg.images.length > 0 ? (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {msg.images.map((img, i) => (
                          <motion.img
                            key={i}
                            src={typeof img === "string" ? img : img.preview}
                            alt={`Message image ${i + 1}`}
                            className="w-full h-40 object-cover rounded-md shadow-sm cursor-pointer"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            onClick={() => handleImageClick(typeof img === "string" ? img : img.preview)}
                            onError={(e) => console.error(`Failed to load image: ${img}`, e)}
                          />
                        ))}
                      </div>
                    ) : (
                      msg.isBot && <p className="text-sm text-gray-500">No images received</p>
                    )}
                  </motion.div>
                </motion.div>
              ))}
              {isLoading && (
                <motion.div
                  className="flex justify-start mb-4"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="max-w-[70%] p-4 rounded-xl bg-gray-200 text-gray-600 shadow-md flex items-center">
                    <span className="mr-2">Thinking...</span>
                    <motion.div
                      className="w-2 h-2 bg-gray-600 rounded-full"
                      animate={{ scale: [1, 1.5, 1] }}
                      transition={{ repeat: Infinity, duration: 0.5 }}
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </motion.div>

          {/* Fixed Input Area */}
          <motion.div
            className="fixed bottom-0 left-0 right-0 max-w-4xl mx-auto px-4 pb-6 z-10 bg-white backdrop-blur-md rounded-t-2xl shadow-xl border border-gray-200"
            variants={inputVariants}
          >
            {/* Image Previews */}
            <AnimatePresence>
              {inputImages.length > 0 && (
                <motion.div
                  className="grid grid-cols-3 gap-3 mb-4 pt-4 px-6"
                  initial="hidden"
                  animate="visible"
                  variants={containerVariants}
                >
                  {inputImages.map((img, index) => (
                    <motion.div
                      key={index}
                      variants={messageVariants}
                      className="relative w-full aspect-square"
                    >
                      <img
                        src={img.preview}
                        alt={`Preview ${index + 1}`}
                        className="w-full h-full object-cover rounded-md shadow-sm"
                      />
                      <motion.button
                        onClick={() => removeImage(index)}
                        className="absolute top-2 right-2 bg-red-500 text-white p-1.5 rounded-full shadow-md"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        <XMarkIcon className="w-4 h-4" />
                      </motion.button>
                    </motion.div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Upload Options and Input */}
            <div className="flex items-end space-x-3 relative px-6 pb-2">
              <motion.div className="flex-shrink-0 relative" whileHover={{ scale: 1.05 }}>
                <button
                  onClick={() => setShowUploadOptions(!showUploadOptions)}
                  className="p-2.5 border-2 border-dashed rounded-lg bg-gray-50 text-gray-500 hover:bg-gray-100 transition-all duration-300"
                  disabled={isLoading}
                >
                  <PhotoIcon className="w-6 h-6" />
                </button>
                <AnimatePresence>
                  {showUploadOptions && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="absolute bottom-12 left-0 bg-white rounded-lg shadow-lg p-2 z-10 border border-gray-200"
                    >
                      <motion.button
                        onClick={() => setShowGalleryModal(true)}
                        className="flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 rounded-md"
                        variants={optionVariants}
                        initial="hidden"
                        animate="visible"
                        exit="exit"
                      >
                        <GalleryIcon className="w-5 h-5 mr-2 text-indigo-500" />
                        Gallery
                      </motion.button>
                      <motion.div
                        {...getRootProps()}
                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 rounded-md cursor-pointer"
                        variants={optionVariants}
                        initial="hidden"
                        animate="visible"
                        exit="exit"
                      >
                        <input {...getInputProps()} />
                        <DocumentIcon className="w-5 h-5 mr-2 text-indigo-500" />
                        File
                      </motion.div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>

              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
                placeholder="Type your message or drop images..."
                className="flex-1 p-3 border border-gray-200 rounded-lg bg-white/50 text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-400 resize-none shadow-sm"
                rows={2}
                disabled={isLoading}
              />
              <motion.button
                onClick={handleSend}
                className="flex-shrink-0 p-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition-all duration-300 shadow-md"
                disabled={isLoading || (!inputText.trim() && inputImages.length === 0)}
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
              >
                <PaperAirplaneIcon className="w-6 h-6" />
              </motion.button>
            </div>
          </motion.div>
        </main>

        {/* Enlarged Image Modal */}
        <AnimatePresence>
          {enlargedImage && (
            <motion.div
              className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={closeEnlargedImage}
            >
              <motion.div
                className="relative w-full max-w-4xl max-h-[80vh] bg-white rounded-lg shadow-xl overflow-hidden"
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.8 }}
                onClick={(e) => e.stopPropagation()}
              >
                <motion.img
                  src={enlargedImage}
                  alt="Enlarged image"
                  className="w-full h-full max-w-full max-h-full object-contain rounded-lg"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                />
                <motion.button
                  onClick={closeEnlargedImage}
                  className="absolute top-2 right-2 bg-gray-800 text-white p-2 rounded-full shadow-md"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <XMarkIcon className="w-6 h-6" />
                </motion.button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Gallery Modal */}
        <AnimatePresence>
          {showGalleryModal && (
            <motion.div
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
              initial="hidden"
              animate="visible"
              exit="exit"
              variants={modalVariants}
              onClick={() => setShowGalleryModal(false)}
            >
              <motion.div
                className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden p-6 flex flex-col relative"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-2xl font-bold text-gray-800">Select One Image from Gallery</h2>
                  <button
                    onClick={() => setShowGalleryModal(false)}
                    className="p-2 text-gray-500 hover:text-gray-700"
                  >
                    <XMarkIcon className="w-6 h-6" />
                  </button>
                </div>
                <div className="flex-1 overflow-y-auto mb-16">
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                    {galleryImages.map((image) => (
                      <motion.div
                        key={image.src}
                        className={`relative aspect-square rounded-lg overflow-hidden shadow-md cursor-pointer ${
                          selectedGalleryImages.some((img) => img.src === image.src)
                            ? "ring-2 ring-indigo-500"
                            : ""
                        }`}
                        whileHover={{ scale: 1.05 }}
                        onClick={() => toggleGalleryImageSelection(image)}
                      >
                        <img
                          src={image.src}
                          alt={image.name || "Gallery image"}
                          className="w-full h-full object-cover"
                        />
                        {selectedGalleryImages.some((img) => img.src === image.src) && (
                          <div className="absolute inset-0 bg-indigo-500 bg-opacity-30 flex items-center justify-center">
                            <motion.svg
                              className="w-8 h-8 text-white"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              transition={{ duration: 0.2 }}
                            >
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                            </motion.svg>
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </div>
                </div>
                {/* Fixed Button Container */}
                <motion.div
                  className="fixed bottom-6 left-0 right-0 max-w-4xl mx-auto px-6 z-10 bg-white"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="flex justify-end space-x-3">
                    <button
                      onClick={() => setShowGalleryModal(false)}
                      className="px-4 py-2 text-gray-600 hover:text-gray-800"
                    >
                      Cancel
                    </button>
                    <motion.button
                      onClick={handleGalleryUpload}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all duration-300"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      disabled={selectedGalleryImages.length === 0}
                    >
                      Upload {selectedGalleryImages.length} Image{selectedGalleryImages.length !== 1 ? "s" : ""}
                    </motion.button>
                  </div>
                </motion.div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Multiple Image Warning Modal */}
        <AnimatePresence>
          {showMultiImageWarning && (
            <motion.div
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={closeMultiImageWarning}
            >
              <motion.div
                className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full"
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.8 }}
                onClick={(e) => e.stopPropagation()}
              >
                <h2 className="text-xl font-bold text-gray-800 mb-4">Multiple Images Not Allowed</h2>
                <p className="text-gray-600 mb-6">You can only upload one image at a time. Please select a single image and try again.</p>
                <div className="flex justify-end">
                  <motion.button
                    onClick={closeMultiImageWarning}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    OK
                  </motion.button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </SubpageLayout>
  );
};

export default Chatbot;