# SmartStudent AI

**AI for Daily Life Transformation Challenge**

## Overview

**SmartStudent AI** is a web application designed specifically for students, assisting them in both academic pursuits and daily life. The platform leverages Retrieval-Augmented Generation (RAG) in combination with large language models (LLMs) to provide intelligent support across key domains:

- **Study Planning and Exam Preparation**
- **Budget Optimization (Tunisian Dinar – TND)**
- **Academic Stress Management**

The system offers seamless integration with several LLM providers, including OpenAI, Groq, Gemini, and Gemma. The frontend features a modern React interface, complete with a floating chatbot for real-time assistance.

---

## Key Features

### AI Chatbot

- Contextual and accurate responses to student queries using RAG-enhanced LLMs.

### RAG-Powered Backend

- Retrieves relevant documents and injects contextual knowledge into AI responses, enhancing both accuracy and relevance.

### Multi-Provider LLM Support

- Effortless switching between major providers:
  - OpenAI
  - Groq
  - Gemini
  - Gemma

### Budget Optimizer (TND)

- Analyze monthly income and expenses in Tunisian Dinar (TND)
- Identify unnecessary spending
- Discover potential savings
- Receive personalized financial recommendations

### Modern Frontend

- Developed using React
- Floating chatbot interface
- Interactive budget planning tools

### Comprehensive Error Handling

- Robust management of:
  - API errors
  - Invalid model configurations
  - Quota and rate limit issues

---

## Important Gemini Integration Note

If you select Gemini as the active model, ensure you update the Gemini API key:

1. Generate a valid Gemini API key.
2. Add it to `backend/.env`.
3. Restart the backend server.

The previously used API key was declined due to security restrictions.

---

## Architecture Overview

### Backend (FastAPI – Python)

- Loads API keys and model configuration from `.env`
- Implements RAG modules for document retrieval and embeddings
- Integrates selected LLM provider for response generation
- Exposes REST endpoints for chat and budget analysis

### Frontend (React)

- Floating AI chatbot for immediate interaction
- Budget optimizer interface (default currency: TND)
- Integrates with backend APIs

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd SmartStudent-AI
```

### 2. Install Dependencies

#### Backend

```bash
pip install -r backend/requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

### 3. Configure Environment Variables

Create or update the `backend/.env` file using the provided example:

```bash
cp backend/.env.example backend/.env
```

Add your LLM provider API keys:

```
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Ensure the Gemini key is valid if you plan to use Gemini as the active model.

### 4. Run the Application

#### Start Backend

```bash
cd backend
python main.py
```

#### Start Frontend

```bash
cd frontend
npm start
```

### 5. Access the Application

Navigate to [http://localhost:3000](http://localhost:3000) in your browser.

---

## Project Structure

```
SmartStudent-AI/
│
├── backend/        # FastAPI server, RAG modules, LLM client, routers, services
├── frontend/       # React application, chatbot UI, budget optimizer
├── demo/           # Demo scenarios and sample data
└── README.md
```

---

## Example Usage

### Chatbot Queries

- *Comment préparer mes examens efficacement ?*

### Budget Optimizer

- Set monthly income to **300 TND**  
- Add expenses  
- Analyze savings and recommendations  

---

## License

This project is intended for educational and demonstration purposes.
