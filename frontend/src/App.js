import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import StudyPlanner from './pages/StudyPlanner';
import BudgetOptimizer from './pages/BudgetOptimizer';
import Dashboard from './pages/Dashboard';
import Chatbot from './pages/Chatbot';
import './App.css';

export default function App() {
  return (
    <Router>
      <Toaster position="top-right" toastOptions={{ style: { background: '#1e1e2e', color: '#e2e8f0', border: '1px solid #6366f1' } }} />
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/study" element={<StudyPlanner />} />
            <Route path="/budget" element={<BudgetOptimizer />} />
          </Routes>
        </main>
        <Chatbot />
      </div>
    </Router>
  );
}

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <span className="logo-icon">🎓</span>
        <div>
          <div className="logo-title">SmartStudent</div>
          <div className="logo-sub">AI Assistant</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/" end className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <span>🏠</span> Dashboard
        </NavLink>
        <NavLink to="/study" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <span>📚</span> Study Planner
        </NavLink>
        <NavLink to="/budget" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <span>💰</span> Budget Optimizer
        </NavLink>
        <div className="nav-item nav-chat-hint">
          <span>🤖</span> AI Chat
          <span className="chat-hint-badge">↘</span>
        </div>
      </nav>
      <div className="sidebar-footer">
        <div className="footer-badge">Hackathon 2026</div>
      </div>
    </aside>
  );
}
