import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { healthAPI } from '../api';

export default function Dashboard() {
  const [apiOk, setApiOk] = useState(null);

  useEffect(() => {
    healthAPI.check()
      .then(() => setApiOk(true))
      .catch(() => setApiOk(false));
  }, []);

  return (
    <div>
      <div className="page-header">
        <div className="page-title">🎓 SmartStudent AI</div>
        <div className="page-sub">Your AI-powered daily life transformation platform</div>
      </div>

      {/* API Status */}
      <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <div style={{
          width: 10, height: 10, borderRadius: '50%',
          background: apiOk === null ? '#6b7280' : apiOk ? '#34d399' : '#f87171'
        }} />
        <span style={{ fontSize: '0.82rem', color: '#9ca3af' }}>
          API {apiOk === null ? 'checking…' : apiOk ? 'connected ✓' : 'offline – start the backend!'}
        </span>
      </div>

      {/* Module Cards */}
      <div className="grid-2" style={{ marginBottom: '2rem' }}>
        <ModuleCard
          icon="📚"
          title="AI Study Planner"
          desc="Input your exams and projects. Get an optimized day-by-day study schedule with priority rankings and smart AI recommendations."
          link="/study"
          color="#4338ca"
          features={['Priority ranking by urgency', 'Daily workload balancing', 'Overload detection', 'AI-powered tips']}
        />
        <ModuleCard
          icon="💰"
          title="AI Budget Optimizer"
          desc="Enter your income and expenses. Receive waste detection, savings estimates, and personalized money-saving strategies."
          link="/budget"
          color="#065f46"
          features={['Category benchmarking', 'Waste detection', 'Annual projection', 'AI savings suggestions']}
        />
      </div>

      {/* Score Formula */}
      <div className="card">
        <div style={{ fontWeight: 600, color: '#a5b4fc', marginBottom: '0.75rem', fontSize: '1rem' }}>
          🏆 Student Efficiency Score (SES) Formula
        </div>
        <div style={{ fontFamily: 'monospace', background: '#0f0f1a', borderRadius: 8, padding: '1rem', fontSize: '0.85rem', color: '#c7d2fe', lineHeight: 2 }}>
          <div>SES = (W_study × study_score + W_budget × budget_score) × 100</div>
          <div style={{ color: '#6b7280', marginTop: '0.5rem' }}>
            study_score  = 1 − (overloaded_days / total_plan_days)<br />
            budget_score = min(savings_rate / 0.20, 1.0)<br />
            W_study = W_budget = 0.5  →  equally weighted
          </div>
        </div>
        <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {[['90-100','Excellent 🟢'],['70-89','Good 🟡'],['50-69','Fair 🟠'],['< 50','Needs Work 🔴']].map(([r,l]) => (
            <span key={r} style={{ fontSize: '0.8rem', color: '#9ca3af' }}><strong style={{ color: '#e2e8f0' }}>{r}</strong> → {l}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ icon, title, desc, link, color, features }) {
  return (
    <div className="card" style={{ borderColor: color, display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <div style={{ fontSize: '2rem' }}>{icon}</div>
      <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#e2e8f0' }}>{title}</div>
      <div style={{ color: '#9ca3af', fontSize: '0.875rem', lineHeight: 1.6 }}>{desc}</div>
      <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
        {features.map(f => (
          <li key={f} style={{ fontSize: '0.82rem', color: '#a5b4fc' }}>✓ {f}</li>
        ))}
      </ul>
      <Link to={link}>
        <button className="btn-primary" style={{ width: '100%', marginTop: '0.5rem' }}>
          Open {title} →
        </button>
      </Link>
    </div>
  );
}
