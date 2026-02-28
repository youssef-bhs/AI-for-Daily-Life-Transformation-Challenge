# AI for Daily Life Transformation Challenge

**Target Audience:** Students

# SmartStudent AI Hackathon Project

## Description
SmartStudent AI is a student-focused web application that leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to help students with study planning, budget optimization (in Tunisian Dinar - TND), and academic stress management. The project supports multiple LLM providers (OpenAI, Groq, Gemini/Gemma) and features a floating chatbot UI for instant assistance.

## Features
- **AI Chatbot**: Answers student questions on study strategies, budgeting, and stress management using RAG and LLMs.
- **RAG Backend**: Retrieves relevant documents and injects context for more accurate answers.
- **Multi-Provider LLM Support**: Easily switch between OpenAI, Groq, Gemini, and Gemma models.
- **Budget Optimizer**: Analyze monthly income and expenses in TND, discover savings, and get personalized advice.
- **Frontend**: Modern React UI with a floating chatbot and interactive budget planner.
- **Error Handling**: Robust feedback for API/model issues and quota limits.

## How It Works
1. **Backend (FastAPI, Python)**
   - Loads API keys and model selection from `.env`.
   - RAG modules retrieve and embed documents for context-aware answers.
   - Chat endpoint integrates LLM responses and sources.
2. **Frontend (React)**
   - Floating chatbot UI for instant Q&A.
   - Budget optimizer with TND as default currency.
   - API integration for chat and budget analysis.

## Setup & Usage
1. **Install dependencies**
   - Backend: `pip install -r backend/requirements.txt`
   - Frontend: `cd frontend && npm install`
2. **Configure API keys**
   - Add your LLM provider keys to `backend/.env` (see example in `.env.example`).
3. **Run the project**
   - Backend: `cd backend && python main.py`
   - Frontend: `cd frontend && npm start`
4. **Access the app**
   - Open [http://localhost:3000](http://localhost:3000) in your browser.

## File Structure
- `backend/` - FastAPI server, RAG modules, LLM client, routers, services
- `frontend/` - React app, chatbot UI, budget optimizer
- `demo/` - Demo scenarios and sample data

## Example Usage
- Ask the chatbot: "Comment préparer mes examens efficacement ?"
- Use the budget optimizer: Set monthly income to 300 TND and add expenses to analyze your budget.

## Authors
- Project by [Your Name]

## License
MIT
