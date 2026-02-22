# RAG Chatbot Setup Guide

This guide explains how to set up and deploy the RAG (Retrieval-Augmented Generation) chatbot for the AI-Native Textbook.

## Architecture

The chatbot system consists of:

1. **Backend API** (FastAPI)
   - RAG service for document embedding and retrieval
   - Qdrant vector database for semantic search
   - OpenAI API for embeddings and chat completion

2. **Frontend** (Docusaurus + React)
   - Chatbot widget embedded in all pages
   - Real-time chat interface
   - Source citation display

3. **Vector Database** (Qdrant)
   - Stores document embeddings
   - Supports filtered search by chapter/section

## Local Development Setup

### 1. Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for running Qdrant locally)

### 2. Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or use Qdrant Cloud (free tier):
1. Sign up at https://cloud.qdrant.io
2. Create a cluster
3. Get your API key and URL

### 3. Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your credentials:

```env
OPENAI_API_KEY=sk-your-key-here
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty for local, add for cloud
DATABASE_URL=postgresql://...
```

### 4. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Index Content

```bash
cd backend
python scripts/index_content.py --docs-dir ../docs/docs --chapter-id intro
```

### 6. Start Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Start Frontend

```bash
cd docs
npm install
npm start
```

The chatbot will appear in the bottom-right corner of the Docusaurus site.

## Deployment

### Vercel (Frontend)

The Docusaurus site is already configured for Vercel deployment. The chatbot will connect to the backend API.

### Backend Deployment Options

#### Option 1: Railway

1. Create a new Railway project
2. Connect your GitHub repository
3. Set root directory to `backend`
4. Add environment variables from `.env.example`
5. Deploy

#### Option 2: Render

1. Create new Web Service
2. Connect GitHub repository
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

#### Option 3: Docker

```bash
cd backend
docker build -t ai-native-backend .
docker run -p 8000:8000 --env-file .env ai-native-backend
```

## API Endpoints

### Chat

```
POST /api/rag/chat
Content-Type: application/json

{
  "message": "What is Physical AI?",
  "conversation_history": [],
  "chapter_id": "intro",  // optional
  "section_id": "overview",  // optional
  "selected_text": "..."  // optional
}
```

### Index Document

```
POST /api/rag/index
Content-Type: application/json

{
  "content": "Document text to index...",
  "chapter_id": "intro",
  "section_id": "overview",
  "metadata": {}
}
```

### Health Check

```
GET /api/rag/health
```

## Troubleshooting

### Chatbot not appearing

1. Check browser console for errors
2. Verify Docusaurus theme Root.js is loaded
3. Check CSS is imported

### "Backend not available" error

1. Ensure backend is running
2. Check API_BASE_URL in Chatbot.tsx
3. Verify CORS settings in backend

### No results from search

1. Check if content is indexed: `GET /api/rag/health`
2. Re-run indexing script
3. Verify Qdrant connection

### OpenAI API errors

1. Check API key in `.env`
2. Verify billing is enabled on OpenAI account
3. Check rate limits

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` |
| `QDRANT_API_KEY` | Qdrant API key (cloud) | `""` |
| `DATABASE_URL` | PostgreSQL connection | Required |
| `RAG_TOP_K` | Number of chunks to retrieve | `5` |
| `RAG_MAX_TOKENS` | Max tokens in response | `1024` |
| `CORS_ORIGINS` | Allowed origins | `["http://localhost:3000"]` |

## Performance Tuning

- Increase `RAG_TOP_K` for more context (slower)
- Use `gpt-4o-mini` for faster, cheaper responses
- Enable Qdrant HNSW index for large datasets
- Cache frequent queries with Redis
