// hooks/useDropzoneHandler.js

import { useDropzone } from "react-dropzone";

const useDropzoneHandler = (setInputImages) => {
  const onDrop = (acceptedFiles) => {
    const newImages = acceptedFiles.map((file) =>
      Object.assign(file, { preview: URL.createObjectURL(file) })
    );
    setInputImages((prev) => [...prev, ...newImages]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: true,
  });

  return { getRootProps, getInputProps };
};

// Exporting as Default
export default useDropzoneHandler;
