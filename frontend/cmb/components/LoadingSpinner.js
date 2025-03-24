import { motion } from "framer-motion";

const LoadingSpinner = () => {
  return (
    <motion.div
      className="text-center text-gray-500 mt-2"
      animate={{ rotate: 360 }}
      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
    >
      ⏳
      <span className="ml-2">Bot is typing...</span>
    </motion.div>
  );
};

export default LoadingSpinner;
