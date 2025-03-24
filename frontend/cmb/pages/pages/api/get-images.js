export default async function handler(req, res) {
  const { filename } = req.query;

  try {
    // ✅ Fetch the image from FastAPI static server
    const imageUrl = `http://localhost:8000/images/${filename}`;

    const response = await fetch(imageUrl);
    if (!response.ok) {
      throw new Error('Image not found');
    }

    // ✅ Set Content-Type dynamically based on image response
    res.setHeader('Content-Type', response.headers.get('Content-Type') || 'image/jpeg');

    // ✅ Convert response to a buffer and send to client
    const buffer = await response.arrayBuffer();
    res.send(Buffer.from(buffer));
  } catch (error) {
    console.error('Error fetching image:', error);
    res.status(404).json({ error: 'Image not found' });
  }
}
