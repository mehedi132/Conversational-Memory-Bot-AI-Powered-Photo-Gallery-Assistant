"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { CloudArrowUpIcon, CheckCircleIcon, ExclamationCircleIcon } from "@heroicons/react/24/outline";
import Navbar from "../components/Navbar";

export default function BatchUploader() {
  const [files, setFiles] = useState([]);
  const [uploadedImages, setUploadedImages] = useState([]);
  const [metadata, setMetadata] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    setFiles(
      acceptedFiles.map((file) =>
        Object.assign(file, { preview: URL.createObjectURL(file) })
      )
    );
    setUploadError(null);
  }, []);

  const handleUpload = async () => {
    if (files.length === 0) return;

    setIsUploading(true);
    setUploadError(null);

    const formData = new FormData();
    files.forEach((file) => formData.append("file", file));

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed with status: " + response.status);

      const data = await response.json();

      setUploadedImages((prev) => [...prev, ...files]);
      setMetadata((prev) => [...prev, ...data.metadata]);
      setFiles([]);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadError("Failed to upload images. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: true,
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
      <Navbar />
      <main className="flex-grow max-w-7xl mx-auto px-4 py-12">
        <motion.section initial="hidden" animate="visible" className="space-y-8">
          <motion.div className="text-center">
            <h1 className="text-4xl font-bold text-gray-800 font-serif">
              Batch Image Uploader
            </h1>
            <p className="mt-2 text-gray-600 text-lg">
              Upload multiple images with ease
            </p>
          </motion.div>

          <motion.div>
            <div
              {...getRootProps()}
              className={`w-full max-w-2xl mx-auto p-8 border-2 border-dashed rounded-xl transition-all duration-300 ${
                isDragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-white hover:border-gray-400"
              }`}
              role="button"
              aria-label="Drag and drop images or click to select"
            >
              <input {...getInputProps()} />
              <div className="flex flex-col items-center space-y-4">
                <CloudArrowUpIcon className="w-12 h-12 text-gray-400" />
                <p className="text-gray-500 text-sm md:text-base">
                  {isDragActive ? "Drop your images here!" : "Drag & drop images here, or click to select"}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Previews in Static Position */}
          <div className="space-y-6">
            <AnimatePresence>
              {files.length > 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="bg-white p-4 rounded-lg shadow-lg"
                >
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 max-h-64 overflow-y-auto">
                    {files.map((file) => (
                      <motion.div key={file.name} className="relative w-full aspect-square">
                        <img
                          src={file.preview}
                          alt={`Preview of ${file.name}`}
                          className="w-full h-full object-cover rounded-md border shadow-sm"
                        />
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Fixed Buttons and Progress Bar */}
          <div className="fixed bottom-10 left-0 right-0 z-10 max-w-7xl mx-auto px-4">
            <AnimatePresence>
              {files.length > 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex justify-center space-x-4 mb-4"
                >
                  <button
                    onClick={handleUpload}
                    disabled={isUploading}
                    className={`px-6 py-2 rounded-md text-white font-medium transition-all duration-300 ${
                      isUploading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
                    }`}
                  >
                    {isUploading ? "Uploading..." : `Upload ${files.length} Image${files.length > 1 ? "s" : ""}`}
                  </button>
                  <button
                    onClick={() => setFiles([])}
                    className="px-6 py-2 rounded-md text-gray-700 bg-gray-200 hover:bg-gray-300 transition-all duration-300"
                  >
                    Clear
                  </button>
                </motion.div>
              )}
            </AnimatePresence>

            <AnimatePresence>
              {isUploading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="max-w-2xl mx-auto"
                >
                  <div className="bg-gray-200 rounded-full h-2.5 overflow-hidden">
                    <motion.div
                      className="bg-blue-600 h-2.5"
                      initial={{ width: "0%" }}
                      animate={{ width: "100%" }}
                      transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    />
                  </div>
                  <p className="text-center text-sm text-gray-600 mt-2">
                    Uploading images, please wait...
                  </p>
                </motion.div>
              )}
            </AnimatePresence>

            <AnimatePresence>
              {uploadError && (
                <motion.div className="flex items-center justify-center text-red-600 mt-4">
                  <ExclamationCircleIcon className="w-5 h-5 mr-2" />
                  <p>{uploadError}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.section>

        {/* Uploaded Images Section */}
        <motion.section className="mt-8">
          {uploadedImages.length > 0 && (
            <>
              <motion.h2 className="text-2xl font-semibold text-gray-700 mb-6 text-center">
                Uploaded Images & Metadata
              </motion.h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                {uploadedImages.map((file, index) => (
                  <motion.div key={index} className="relative w-full aspect-square overflow-hidden rounded-xl shadow-lg">
                    <img src={file.preview} alt={`Uploaded image ${index + 1}`} className="w-full h-full object-cover" />
                    <div className="absolute top-2 right-2 bg-green-500/80 rounded-full p-1">
                      <CheckCircleIcon className="w-5 h-5 text-white" />
                    </div>
                    <div className="p-2 bg-white shadow-md rounded-md mt-2 text-center">
                      <p className="text-gray-700 text-sm font-semibold">
                        {metadata[index]?.description || "No description"}
                      </p>
                      <p className="text-xs text-gray-500">{metadata[index]?.tags?.join(", ") || "No tags"}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </>
          )}
        </motion.section>
      </main>
    </div>
  );
}