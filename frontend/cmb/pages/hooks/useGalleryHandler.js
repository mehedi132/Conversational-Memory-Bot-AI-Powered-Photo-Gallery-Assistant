import { useState, useEffect } from "react";

const useGalleryHandler = (setInputImages, setShowUploadOptions) => {
  const [showGalleryModal, setShowGalleryModal] = useState(false);
  const [galleryImages, setGalleryImages] = useState([]);
  const [selectedGalleryImages, setSelectedGalleryImages] = useState([]);

  // Fetch gallery images when modal opens
  useEffect(() => {
    if (showGalleryModal) {
      const fetchGalleryImages = async () => {
        try {
          const response = await fetch("/api/gallery-images");
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

  // Handle gallery image selection
  const toggleGalleryImageSelection = (image) => {
    setSelectedGalleryImages((prev) =>
      prev.some((img) => img.src === image.src)
        ? prev.filter((img) => img.src !== image.src)
        : [...prev, image]
    );
  };

  // Handle upload from gallery
  const handleGalleryUpload = () => {
    setInputImages((prev) => [
      ...prev,
      ...selectedGalleryImages.map((img) => ({ preview: img.src })),
    ]);
    setShowGalleryModal(false);
    setSelectedGalleryImages([]);
    setShowUploadOptions(false);
  };

  return {
    showGalleryModal,
    setShowGalleryModal,
    galleryImages,
    selectedGalleryImages,
    toggleGalleryImageSelection,
    handleGalleryUpload,
  };
};

export default useGalleryHandler;
