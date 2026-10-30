
# AI PDF Chatbot Using RAG

An AI-powered PDF question-answering application built with Django, Retrieval-Augmented Generation (RAG), ChromaDB, Sentence Transformers, and Google Gemini API.

Users can upload PDF documents and ask questions in natural language. The application retrieves relevant information from the uploaded document and generates context-aware answers using an LLM.

## Features

- PDF Upload: Upload PDF documents through a Django web interface.
- PDF Text Extraction: Extract text from PDF pages using PyMuPDF.
- Text Chunking: Split extracted text into smaller chunks using Recursive Character Text Splitter.
- Embeddings Generation: Convert text chunks into vector embeddings using Sentence Transformers.
- Vector Database: Store and retrieve document embeddings using ChromaDB.
- Semantic Search: Find relevant PDF content based on user questions.
- AI-Powered Answers: Generate answers using Google Gemini API.
- Conversation Memory: Store previous questions and AI responses using Django ORM.
- Follow-up Questions: Maintain conversation context for follow-up questions.
- Source References: Display relevant PDF page numbers.
- Responsive Interface: ChatGPT-inspired chat interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| PyMuPDF | PDF text extraction |
| LangChain Text Splitters | Text chunking |
| Sentence Transformers | Embeddings generation |
| ChromaDB | Vector database |
| Google Gemini API | AI answer generation |
| SQLite | Conversation and message storage |
| HTML, CSS, JavaScript | Frontend |

## Project Architecture

```text
User
 |
 v
Django Web Application
 |
 v
PDF Upload
 |
 v
PDF Text Extraction
 |
 v
Text Chunking
 |
 v
Embedding Generation
 |
 v
ChromaDB Vector Database
 |
 v
User Question
 |
 v
Question Embedding
 |
 v
Semantic Search
 |
 v
Relevant PDF Chunks
 |
 v
Google Gemini API
 |
 v
AI Generated Answer
 |
 v
Display Answer and Source Pages
```

## Project Structure

```text
pdf_chat_rag/
|
|-- chatbot/
|   |-- migrations/
|   |-- services/
|   |   |-- __init__.py
|   |   |-- rag_service.py
|   |   |-- search_service.py
|   |   |-- gemini_service.py
|   |
|   |-- templates/
|   |   |-- chatbot/
|   |       |-- upload.html
|   |       |-- extracted_text.html
|   |       |-- search.html
|   |
|   |-- models.py
|   |-- forms.py
|   |-- views.py
|   |-- urls.py
|
|-- config/
|   |-- settings.py
|   |-- urls.py
|
|-- media/
|-- chroma_db/
|-- manage.py
|-- requirements.txt
|-- .env
|-- .gitignore
|-- README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/django-pdf-rag-chatbot.git
```

### 2. Navigate to the Project Directory

```bash
cd django-pdf-rag-chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

For Linux/macOS:

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Get your API key from Google AI Studio:

https://aistudio.google.com/

Never upload your actual API key to GitHub.

### 7. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Start the Django Development Server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## How It Works

### Document Processing

1. User uploads a PDF.
2. PyMuPDF extracts text from each page.
3. Recursive Character Text Splitter divides text into smaller chunks.
4. Sentence Transformers generates embeddings.
5. ChromaDB stores chunks, embeddings, and metadata.

### Question Answering

1. User selects an uploaded PDF.
2. User enters a question.
3. Sentence Transformers converts the question into an embedding.
4. ChromaDB performs semantic similarity search.
5. Relevant text chunks are retrieved.
6. Retrieved context and conversation history are sent to Gemini.
7. Gemini generates an answer based on the PDF context.
8. The application displays the answer and source page references.

## Future Improvements

- Improve Gemini API response time.
- Add streaming AI responses.
- Improve contextual retrieval for follow-up questions.
- Add conversation management and chat history sidebar.
- Support multiple document formats.
- Add user authentication.
- Deploy the application to a cloud server.
- Improve error handling and API reliability.

## Current Limitations

- AI response time depends on Gemini API latency and network conditions.
- Current retrieval uses semantic similarity and a configurable distance threshold.
- Follow-up question retrieval can be improved through contextual query rewriting.
- Application is currently designed as a development project and needs further optimization before production deployment.

## Author

**Gurucharan Lovanshi**

B.Tech Computer Science Engineering

GitHub: https://github.com/gurucharan1

---

If you find this project useful, feel free to explore the repository and share feedback.
