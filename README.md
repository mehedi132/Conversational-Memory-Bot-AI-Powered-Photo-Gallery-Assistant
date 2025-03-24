# Conversational Memory Bot – AI-Powered Photo Gallery Assistant

Welcome to the **Conversational Memory Bot**, an AI-powered chatbot that redefines how you interact with your personal photo galleries! By combining cutting-edge Natural Language Processing (NLP) and multimodal AI, this project lets you query, retrieve, and explore your photos using everyday language and visual features. Whether you're reminiscing about a trip, cataloging events, or searching for specific moments, this bot makes it intuitive and fun.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [System Workflow](#system-workflow)
- [How to Run the Project](#how-to-run-the-project)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Conversational Memory Bot transforms your photo gallery into an interactive, conversational experience. Imagine asking, "Show me photos of my dog playing in the park," and instantly getting relevant images with detailed descriptions—or finding visually similar photos with a single click. Powered by advanced AI, this project bridges text and visuals to make browsing and organizing your memories seamless and engaging.

This repository contains the complete codebase, hosted on GitHub, with a modern frontend built in Next.js and a robust backend powered by FastAPI. Whether you're a user exploring your photos or a developer looking to extend the project, this README will guide you through everything you need to know.

---

## Key Features

Here’s what makes the Conversational Memory Bot stand out:

- **Natural Language Querying**: Ask anything, like "Find pictures from my 2021 Italy trip" or "Show me sunset beaches," and get instant results.
- **Contextual Image Retrieval**: Matches your query to photos using both text context and visual content for spot-on accuracy.
- **Detailed Image Descriptions**: Get rich descriptions, e.g., "This photo shows a golden retriever chasing a ball in a grassy field."
- **Visual Similarity Search**: Discover photos that look alike based on colors, objects, or scenes—perfect for finding hidden gems.
- **Interactive Gallery**: Browse results with zoom, tags, and clickable details in a sleek, user-friendly interface.
- **Relevance Ranking**: See the most relevant images first, thanks to a smart scoring system blending NLP and visual features.

---

## Technologies Used

The Conversational Memory Bot is built with a powerful tech stack:

- **[Next.js](https://nextjs.org/)**: A React framework for a fast, responsive frontend with server-side rendering.
- **[FastAPI](https://fastapi.tiangolo.com/)**: A high-performance Python framework for building the backend API.
- **[LangChain](https://langchain.com/)**: Manages conversational AI, enabling context-aware responses and query handling.
- **[CLIP](https://openai.com/research/clip)**: OpenAI’s model for generating text and image embeddings, bridging language and visuals.
- **[FAISS](https://github.com/facebookresearch/faiss)**: A vector database for lightning-fast similarity searches across image embeddings.
- **[Gemini Free API](https://gemini.google.com/)**: A free-tier language model API for generating natural, human-like responses.

These tools work together to create a seamless, intelligent photo gallery assistant.

---

## System Workflow

Here’s how the magic happens:

1. **Query Processing**:

   - You type a query (e.g., "Show me photos of cats in the garden").
   - The NLP module (LangChain + Gemini) interprets it and creates a text embedding with CLIP.

2. **Image Retrieval**:

   - Precomputed image embeddings (via CLIP) are stored in FAISS.
   - The system matches your query’s embedding to image embeddings, ranking them by similarity.

3. **RAG Pipeline**:

   - Top images are retrieved using semantic search.
   - LangChain and Gemini generate contextual responses based on the images and your query.

4. **Output**:
   - Results appear in an interactive gallery with descriptions, tags, and options to explore further.

---

## How to Run the Project

Ready to try it out? Follow these steps to get the Conversational Memory Bot up and running on your machine.

### Prerequisites

Before you start, ensure you have:

- **Node.js** (v14 or later) - [Download](https://nodejs.org/)
- **Python** (v3.8 or later) - [Download](https://www.python.org/)
- **Git** - [Download](https://git-scm.com/)
- **Gemini API Key** - Sign up at [Gemini](https://gemini.google.com/) to get your free API key.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/mehedi132/Conversational-Memory-Bot-AI-Powered-Photo-Gallery-Assistant.git]
   cd Conversational-Memory-Bot-AI-Powered-Photo-Gallery-Assistant
   Set Up the Frontend (Next.js)
   Here is the complete Markdown code for the provided text, structured for clarity and ease of use in a README.md file:
   ```

## How to Run the Project

### Set Up the Frontend (Next.js)

Navigate to the frontend directory and install the dependencies:

```bash
cd frontend/cmb
npm install
```

### Set Up the Backend (FastAPI)

Navigate to the backend directory and install the required Python packages:

```bash
cd ../backend
pip install -r requirements.txt
```

### Configure Environment Variables

In the backend directory, create a `.env` file with the following content:

```plaintext
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual Gemini API key.

### Run the Application

First, start the backend server:

```bash
cd backend
uvicorn main:app --reload
```

Then, in a new terminal window, start the frontend development server:

```bash
cd frontend/cmb
npm run dev
```

### Access the Bot

Open your web browser and go to [http://localhost:3000](http://localhost:3000). Start querying your photo gallery!

### Troubleshooting

- **API Key Not Working?** Double-check your `.env` file in the backend directory and ensure the Gemini API key is valid.
- **Missing Dependencies?** Rerun `npm install` in the frontend directory or `pip install -r requirements.txt` in the backend directory.
- **Port Already in Use?** Change the port for the backend by running `uvicorn main:app --reload --port 8001`, or adjust the frontend port in the Next.js configuration if 3000 or 8000 are occupied.

## Contributing

Love the project? We’d love your help! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/awesome-improvement
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add awesome improvement"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/awesome-improvement
   ```
5. Open a pull request!

For significant changes, please open an issue first to discuss your ideas with the maintainers.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
