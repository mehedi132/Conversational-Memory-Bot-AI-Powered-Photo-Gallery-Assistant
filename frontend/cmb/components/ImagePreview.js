import { motion } from "framer-motion";
import { XMarkIcon } from "@heroicons/react/24/outline";

const ImagePreview = ({ img, index, removeImage }) => {
  return (
    <motion.div
      key={index}
      className="relative w-full aspect-square"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
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
  );
};

export default ImagePreview;
