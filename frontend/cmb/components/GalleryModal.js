import { motion, AnimatePresence } from "framer-motion";
import { XMarkIcon } from "@heroicons/react/24/outline";

const GalleryModal = ({
  showGalleryModal,
  setShowGalleryModal,
  galleryImages,
  selectedGalleryImages,
  toggleGalleryImageSelection,
  handleGalleryUpload,
}) => {
  return (
    <AnimatePresence>
      {showGalleryModal && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          initial="hidden"
          animate="visible"
          exit="exit"
          onClick={() => setShowGalleryModal(false)}
        >
          <motion.div
            className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[80vh] overflow-y-auto p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">
                Select Images from Gallery
              </h2>
              <button
                onClick={() => setShowGalleryModal(false)}
                className="p-2 text-gray-500 hover:text-gray-700"
              >
                <XMarkIcon className="w-6 h-6" />
              </button>
            </div>
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
                </motion.div>
              ))}
            </div>
            <div className="mt-6 flex justify-end space-x-3">
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
                Upload {selectedGalleryImages.length} Image
                {selectedGalleryImages.length !== 1 ? "s" : ""}
              </motion.button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default GalleryModal;
