import { motion } from "framer-motion";

const MessageBubble = ({ msg }) => {
  return (
    <motion.div
      className={`flex ${msg.isBot ? "justify-start" : "justify-end"} mb-4`}
    >
      <motion.div
        className={`max-w-[70%] p-4 rounded-xl shadow-md ${
          msg.isBot
            ? "bg-gradient-to-r from-blue-100 to-indigo-100 text-gray-800"
            : "bg-gradient-to-r from-blue-500 to-indigo-500 text-white"
        }`}
      >
        {msg.text && <p className="mb-2 text-sm">{msg.text}</p>}
        <p className="text-xs text-gray-500">{msg.timestamp}</p>
        {msg.images.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
            {msg.images.map((img, i) => (
              <img
                key={i}
                src={img.preview}
                alt={`Message image ${i + 1}`}
                className="w-full h-40 object-cover rounded-md shadow-sm"
              />
            ))}
          </div>
        )}
      </motion.div>
    </motion.div>
  );
};

export default MessageBubble;
