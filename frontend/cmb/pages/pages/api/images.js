export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      // Fetch image metadata from FastAPI
      const response = await fetch('http://localhost:8000/api/images');
      if (!response.ok) {
        throw new Error('Failed to fetch image metadata');
      }

      const images = await response.json();
      //console.log(images);  // Check the response in the console
      // Ensure the frontend gets full image URLs
      const updatedImages = images.map(image => ({
        ...image,
        src: `http://localhost:8000${image.src}` // Append base URL
      }));

      res.status(200).json({ images: updatedImages });
    } catch (error) {
      console.error('Error fetching image metadata:', error);
      res.status(500).json({ error: 'Error fetching image metadata' });
    }
  } else {
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}
