SmartStudent AI

AI for Daily Life Transformation Challenge
Target Audience: Students

Overview

SmartStudent AI is a student-focused web application designed to assist students in their academic and daily lives. The platform combines Retrieval-Augmented Generation (RAG) with Large Language Models (LLMs) to provide intelligent support in:

Study planning and exam preparation

Budget optimization (in Tunisian Dinar – TND)

Academic stress management

The system supports multiple LLM providers, including OpenAI, Groq, and Gemini/Gemma, and features a modern React interface with a floating chatbot for real-time assistance.

Key Features
AI Chatbot

Provides contextual and accurate responses to student questions using RAG-enhanced LLMs.

RAG-Powered Backend

Retrieves relevant documents and injects contextual knowledge into AI responses to improve accuracy and relevance.

Multi-Provider LLM Support

Easily switch between:

OpenAI

Groq

Gemini

Gemma

Budget Optimizer (TND)

Analyze monthly income and expenses in Tunisian Dinar (TND) to:

Identify unnecessary spending

Discover potential savings

Receive personalized financial recommendations

Modern Frontend

Built with React

Floating chatbot interface

Interactive budget planning tools

Error Handling

Robust handling of:

API errors

Invalid model configurations

Quota and rate limit issues

Important Note

The Gemini API key must be updated before use.

The previously added API key was declined due to security restrictions. To enable Gemini models:

Generate a valid Gemini API key.

Add it to the backend/.env file.

Restart the backend server.

Architecture Overview
Backend (FastAPI – Python)

Loads API keys and model configuration from .env

Implements RAG modules for document retrieval and embeddings

Integrates the selected LLM provider for response generation

Exposes REST endpoints for chat and budget analysis

Frontend (React)

Floating AI chatbot for instant interaction

Budget optimizer interface (default currency: TND)

API integration with backend services

Installation and Setup
1. Clone the Repository
git clone <your-repository-url>
cd SmartStudent-AI
2. Install Dependencies
Backend
pip install -r backend/requirements.txt
Frontend
cd frontend
npm install
3. Configure Environment Variables

Create or update backend/.env using the example file:

backend/.env.example

Add your LLM provider API keys:

OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key

Ensure the Gemini key is valid if selecting Gemini as the active model.

4. Run the Application
Start Backend
cd backend
python main.py
Start Frontend
cd frontend
npm start
5. Access the Application

Open your browser and navigate to:

http://localhost:3000
Project Structure
SmartStudent-AI/
│
├── backend/        # FastAPI server, RAG modules, LLM client, routers, services
├── frontend/       # React application, chatbot UI, budget optimizer
├── demo/           # Demo scenarios and sample data
└── README.md
Example Usage

Ask the chatbot:
"Comment préparer mes examens efficacement ?"

Use the Budget Optimizer:

Set monthly income to 300 TND

Add expenses

Analyze savings and recommendations
