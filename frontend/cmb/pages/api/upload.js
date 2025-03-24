import multer from "multer";
import path from "path";
import fs from "fs";
import FormData from "form-data";
import fetch from "node-fetch";

const uploadDir = path.join(process.cwd(), "public/uploads");

// Ensure the upload directory exists
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// ✅ Configure Multer for Multiple File Uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    // cb(null, `${Date.now()}-${file.originalname}`);
    cb(null, `${file.originalname}`);
  },
});

const upload = multer({ storage }).array("file", 25); // ✅ Accept multiple files under "file"

export const config = {
  api: {
    bodyParser: false, // ✅ Required for Multer to process form-data
  },
};

export default function handler(req, res) {
  if (req.method === "POST") {
    upload(req, res, async (err) => {
      if (err) {
        console.error("Multer error:", err);
        return res.status(500).json({ error: "Upload failed!" });
      }

      try {
        const uploadedFiles = req.files; // ✅ Get all uploaded files
        if (!uploadedFiles || uploadedFiles.length === 0) {
          return res.status(400).json({ error: "No files uploaded!" });
        }

        console.log(
          "Uploading images to FastAPI:",
          uploadedFiles.map((f) => f.path)
        ); // ✅ Debugging

        // ✅ Send Each Image to FastAPI for Processing
        const responses = await Promise.all(
          uploadedFiles.map(async (file) => {
            const formData = new FormData();
            formData.append("file", fs.createReadStream(file.path));

            const fastApiResponse = await fetch(
              "http://localhost:8000/api/process-image/",
              {
                method: "POST",
                body: formData,
                headers: formData.getHeaders(),
              }
            );

            console.log("FastAPI Response Status:", fastApiResponse.status);
            if (!fastApiResponse.ok)
              throw new Error("FastAPI processing failed");

            const responseData = await fastApiResponse.json();
            return responseData.image_metadata;
          })
        );

        // ✅ Delete Temporary Files
        uploadedFiles.forEach((file) => fs.unlinkSync(file.path));

        return res.status(200).json({
          message: "Images uploaded and processed successfully!",
          metadata: responses,
        });
      } catch (error) {
        console.error("Error processing images:", error);
        return res.status(500).json({ error: "Error processing images!" });
      }
    });
  } else {
    return res.status(405).json({ error: "Method Not Allowed" });
  }
}
