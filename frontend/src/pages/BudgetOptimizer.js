import React, { useState } from 'react';
import toast from 'react-hot-toast';
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { budgetAPI } from '../api';

const EMPTY_EXPENSE = { category: '', amount: '', description: '' };

const PIE_COLORS = ['#6366f1','#8b5cf6','#ec4899','#f59e0b','#10b981','#3b82f6','#f87171','#a3e635','#fb923c','#34d399'];

export default function BudgetOptimizer() {
  const [income,   setIncome]   = useState(300);
  const [currency, setCurrency] = useState('TND');
  const [expenses, setExpenses] = useState([{ ...EMPTY_EXPENSE }]);
  const [loading,  setLoading]  = useState(false);
  const [result,   setResult]   = useState(null);

  const addExpense    = () => setExpenses(p => [...p, { ...EMPTY_EXPENSE }]);
  const removeExpense = i  => setExpenses(p => p.filter((_, idx) => idx !== i));
  const updateExpense = (i, field, val) => setExpenses(p => p.map((e, idx) => idx === i ? { ...e, [field]: val } : e));

  const loadSample = async () => {
    const { data } = await budgetAPI.getSample();
    setIncome(data.monthly_income);
    setCurrency(data.currency);
    setExpenses(data.expenses);
    toast.success('Sample data loaded!');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const payload = {
        monthly_income: Number(income),
        currency,
        expenses: expenses.map(ex => ({ ...ex, amount: Number(ex.amount) })),
      };
      const { data } = await budgetAPI.analyze(payload);
      setResult(data);
      toast.success('Budget analysis complete!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-title">💰 AI Budget Optimizer</div>
        <div className="page-sub">Analyze your spending and discover hidden savings</div>
      </div>

      <form onSubmit={handleSubmit}>
        {/* ── Income Row ── */}
        <div className="panel">
          <div className="panel-title">💵 Income</div>
          <div className="form-row">
            <div className="form-group" style={{ maxWidth: 200 }}>
              <label className="form-label">Monthly Income</label>
              <input type="number" min="1" value={income} onChange={e => setIncome(e.target.value)} required />
            </div>
            <div className="form-group" style={{ maxWidth: 100 }}>
              <label className="form-label">Currency</label>
              <select value={currency} onChange={e => setCurrency(e.target.value)}>
                {['TND','USD','EUR','GBP','MAD','DZD','CAD','AUD'].map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
          </div>
        </div>

        {/* ── Expenses Panel ── */}
        <div className="panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div className="panel-title" style={{ margin: 0 }}>📋 Monthly Expenses</div>
            <button type="button" className="btn-secondary" onClick={addExpense}>+ Add Expense</button>
          </div>
          {expenses.map((ex, i) => (
            <div className="form-row" key={i}>
              <div className="form-group">
                <label className="form-label">Category</label>
                <input value={ex.category} onChange={e => updateExpense(i, 'category', e.target.value)}
                  placeholder="e.g. Food, Rent, Entertainment" required />
              </div>
              <div className="form-group" style={{ maxWidth: 130 }}>
                <label className="form-label">Amount ({currency})</label>
                <input type="number" min="0" step="0.01" value={ex.amount}
                  onChange={e => updateExpense(i, 'amount', e.target.value)} required />
              </div>
              <div className="form-group">
                <label className="form-label">Description (optional)</label>
                <input value={ex.description}
                  onChange={e => updateExpense(i, 'description', e.target.value)}
                  placeholder="Brief note" />
              </div>
              {expenses.length > 1 && (
                <button type="button" className="btn-danger" onClick={() => removeExpense(i)}>✕</button>
              )}
            </div>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Analyzing…' : '🔍 Analyze Budget'}
          </button>
          <button type="button" className="btn-secondary" onClick={loadSample}>
            📋 Load Sample Data
          </button>
        </div>
      </form>

      {loading && <div style={{ marginTop: '2rem' }}><div className="spinner" /></div>}
      {result  && <BudgetResult result={result} currency={currency} />}
    </div>
  );
}

function BudgetResult({ result, currency }) {
  const {
    total_expenses, monthly_savings, savings_rate_pct,
    category_breakdown, waste_detected, annual_projection,
    ai_suggestions, student_efficiency_score,
  } = result;

  const pieData = category_breakdown.map(c => ({ name: c.category, value: c.amount }));

  return (
    <div style={{ marginTop: '2rem' }}>
      {/* ── Stats Row ── */}
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-label">Total Expenses</div>
          <div className="stat-value">{currency} {total_expenses.toLocaleString()}</div>
          <div className="stat-sub">this month</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Monthly Savings</div>
          <div className="stat-value" style={{ color: monthly_savings >= 0 ? '#34d399' : '#f87171' }}>
            {currency} {monthly_savings.toLocaleString()}
          </div>
          <div className="stat-sub">{savings_rate_pct}% savings rate</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Efficiency Score</div>
          <div className="stat-value" style={{ color: scoreColor(student_efficiency_score) }}>
            {student_efficiency_score}
          </div>
          <div className="stat-sub">{scoreLabel(student_efficiency_score)}</div>
        </div>
      </div>

      {/* ── Chart + Breakdown ── */}
      <div className="grid-2" style={{ marginBottom: '1.5rem' }}>
        <div className="card">
          <div className="section-title" style={{ marginTop: 0 }}>📊 Spending Breakdown</div>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={55} outerRadius={90}
                dataKey="value" paddingAngle={3}>
                {pieData.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `${currency} ${v}`}
                contentStyle={{ background: '#1e1e2e', border: '1px solid #4338ca', color: '#e2e8f0' }} />
              <Legend wrapperStyle={{ fontSize: '0.78rem', color: '#9ca3af' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="section-title" style={{ marginTop: 0 }}>📈 Category Benchmarks</div>
          {category_breakdown.map((cat, i) => (
            <div className="budget-bar-wrap" key={i}>
              <div className="budget-bar-label">
                <span>{cat.category}</span>
                <span>
                  {currency} {cat.amount} · {cat.percentage}%
                  <span style={{ marginLeft: '0.4rem' }} className={`badge-${cat.status}`}>{cat.status}</span>
                </span>
              </div>
              <div className="budget-bar-track">
                <div
                  className={`budget-bar-fill fill-${cat.status}`}
                  style={{ width: `${Math.min(cat.percentage / 50 * 100, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Waste Detection ── */}
      {waste_detected.length > 0 && (
        <>
          <div className="section-title">🚨 Waste Detected ({waste_detected.length} category{waste_detected.length > 1 ? 'ies' : 'y'})</div>
          {waste_detected.map((w, i) => (
            <div className="waste-card" key={i}>
              <div className="waste-card-header">
                <span className="waste-cat">⚠️ {w.category}</span>
                <span className="waste-excess">+{currency} {w.excess_amount} over limit</span>
              </div>
              <div style={{ fontSize: '0.8rem', color: '#9ca3af', marginBottom: '0.4rem' }}>
                Spending {currency} {w.current_amount} · Recommended max: {currency} {w.recommended_max}
              </div>
              <div className="waste-tip">💡 {w.suggestion}</div>
            </div>
          ))}
        </>
      )}

      {/* ── Annual Projection ── */}
      <div className="section-title">📆 Annual Projection</div>
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-label">Annual Expenses</div>
          <div className="stat-value" style={{ fontSize: '1.2rem' }}>
            {currency} {annual_projection.current_annual_expenses.toLocaleString()}
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Projected Savings</div>
          <div className="stat-value" style={{ fontSize: '1.2rem', color: '#34d399' }}>
            {currency} {annual_projection.projected_annual_savings.toLocaleString()}
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Optimized Savings</div>
          <div className="stat-value" style={{ fontSize: '1.2rem', color: '#a5b4fc' }}>
            {currency} {annual_projection.optimized_annual_savings.toLocaleString()}
          </div>
          <div className="stat-sub">+{currency} {annual_projection.delta.toLocaleString()} if waste cut</div>
        </div>
      </div>

      {/* ── AI Suggestions ── */}
      <div className="ai-box">
        <div className="ai-box-title">🤖 AI Money-Saving Suggestions</div>
        <p>{ai_suggestions}</p>
      </div>
    </div>
  );
}

function scoreColor(score) {
  if (score >= 90) return '#34d399';
  if (score >= 70) return '#fbbf24';
  if (score >= 50) return '#fb923c';
  return '#f87171';
}
function scoreLabel(score) {
  if (score >= 90) return 'Excellent 🟢';
  if (score >= 70) return 'Good 🟡';
  if (score >= 50) return 'Fair 🟠';
  return 'Needs Work 🔴';
}
