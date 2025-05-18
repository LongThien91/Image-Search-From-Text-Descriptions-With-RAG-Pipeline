# Image-Search-From-Text-Descriptions-With-RAG-Pipeline

## 📌  Project Overview

Image Search From Text Descriptions With RAG Pipeline is an intelligent image retrieval system that allows users to search for images using natural language queries. The system combines the power of Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to deliver accurate and context-aware image search results.

## 🔍 How It Works
1. Image Upload & Description Generation
When an image is uploaded, a Large Language Model (LLM) is used to automatically generate a detailed textual description of the image content. Alternatively, users can provide their own custom descriptions for improved accuracy.

2. Vectorization & Storage
The description (generated or user-provided) is embedded into a dense vector using a sentence embedding model and stored in Qdrant, a high-performance vector database. The image itself is uploaded to Cloudinary, and its ID is linked to the corresponding vector in Qdrant.

3. Text-Based Image Retrieval
When a user submits their query (e.g., "a black t-shirt with a big heart and the YOLO logo on it"), the system embeds the query and performs a semantic similarity search in Qdrant to retrieve the top-k most relevant image descriptions.

4. Post-Filtering with LLM for Best Match
After retrieving the top-matching descriptions, the system uses the LLM again to compare each description with the user query  and remove any results that are not really related. Finally, all the best-matching images are selected and all Cloudinary URL are returned to the user.

