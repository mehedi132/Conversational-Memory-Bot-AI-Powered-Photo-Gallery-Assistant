import formidable from "formidable";
import fs from "fs";

export const config = { api: { bodyParser: false } };

export default async function handler(req, res) {
  if (req.method !== "POST") {
    console.log(`Invalid method: ${req.method}`);
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    console.log("Parsing request with formidable...");
    const form = formidable({ multiples: true, keepExtensions: true });
    const [fields, files] = await form.parse(req);

    console.log("Raw fields from formidable:", fields);
    const text = fields.text?.[0] || null;
    const imagePaths = fields.imagePaths?.[0] || null;

    console.log("Raw files from formidable:", files);
    const imageFiles = files.imageFiles || [];

    const formData = new FormData();
    if (text) formData.append("text", text);
    if (imagePaths) formData.append("imagePaths", imagePaths);
    for (const file of imageFiles) {
      const fileData = fs.readFileSync(file.filepath);
      const blob = new Blob([fileData], { type: file.mimetype });
      formData.append("imageFiles", blob, file.originalFilename);
      console.log(`Added image file to formData: ${file.originalFilename}`);
    }

    console.log("Forwarding to FastAPI at http://localhost:8000/api/search");

    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
      console.log("Fetch timed out after 40 seconds");
    }, 1000000); // 30s timeout

    const backendResponse = await fetch("http://localhost:8000/api/search", {
      method: "POST",
      body: formData,
      signal: controller.signal, // Add timeout signal
    }).catch((err) => {
      throw new Error(`Fetch failed: ${err.message} (Type: ${err.name})`);
    });
    clearTimeout(timeoutId); // Clear timeout if fetch succeeds

    console.log("FastAPI response status:", backendResponse.status);

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error("FastAPI error:", errorText);
      throw new Error(
        `FastAPI request failed: ${backendResponse.status} - ${errorText}`
      );
    }

    const data = await backendResponse.json();
    console.log("FastAPI response data:", data);
    res.status(200).json({ text: data.text, images: data.images });
  } catch (error) {
    console.error("Error in /api/chatbot:", error.message, error.stack);
    res.status(500).json({ text: "Server error", images: [] });
  }
}
