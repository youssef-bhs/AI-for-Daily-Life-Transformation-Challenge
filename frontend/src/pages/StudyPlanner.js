import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { studyAPI } from '../api';

const EMPTY_EXAM    = { subject: '', exam_date: '', difficulty: 3 };
const EMPTY_PROJECT = { name: '', deadline: '', estimated_hours: 8 };

export default function StudyPlanner() {
  const [exams,     setExams]     = useState([{ ...EMPTY_EXAM }]);
  const [projects,  setProjects]  = useState([{ ...EMPTY_PROJECT }]);
  const [hoursDay,  setHoursDay]  = useState(4);
  const [startDate, setStartDate] = useState('2026-02-27');
  const [loading,   setLoading]   = useState(false);
  const [result,    setResult]    = useState(null);

  // ── Exam helpers ──
  const addExam = () => setExams(p => [...p, { ...EMPTY_EXAM }]);
  const removeExam = i => setExams(p => p.filter((_, idx) => idx !== i));
  const updateExam = (i, field, val) => setExams(p => p.map((e, idx) => idx === i ? { ...e, [field]: val } : e));

  // ── Project helpers ──
  const addProject = () => setProjects(p => [...p, { ...EMPTY_PROJECT }]);
  const removeProject = i => setProjects(p => p.filter((_, idx) => idx !== i));
  const updateProject = (i, field, val) => setProjects(p => p.map((e, idx) => idx === i ? { ...e, [field]: val } : e));

  // ── Load sample ──
  const loadSample = async () => {
    const { data } = await studyAPI.getSample();
    setExams(data.exams);
    setProjects(data.projects);
    setHoursDay(data.available_hours_per_day);
    setStartDate(data.start_date);
    toast.success('Sample data loaded!');
  };

  // ── Submit ──
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const payload = {
        exams: exams.map(ex => ({ ...ex, difficulty: Number(ex.difficulty) })),
        projects: projects.map(p => ({ ...p, estimated_hours: Number(p.estimated_hours) })),
        available_hours_per_day: Number(hoursDay),
        start_date: startDate || undefined,
      };
      const { data } = await studyAPI.generatePlan(payload);
      setResult(data);
      toast.success('Study plan generated!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-title">📚 AI Study Planner</div>
        <div className="page-sub">Generate your optimized study schedule in seconds</div>
      </div>

      <form onSubmit={handleSubmit}>
        {/* ── Exams Panel ── */}
        <div className="panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div className="panel-title" style={{ margin: 0 }}>📝 Exams</div>
            <button type="button" className="btn-secondary" onClick={addExam}>+ Add Exam</button>
          </div>
          {exams.map((ex, i) => (
            <div className="form-row" key={i}>
              <div className="form-group">
                <label className="form-label">Subject</label>
                <input value={ex.subject} onChange={e => updateExam(i, 'subject', e.target.value)}
                  placeholder="e.g. Mathematics" required />
              </div>
              <div className="form-group" style={{ maxWidth: 150 }}>
                <label className="form-label">Exam Date</label>
                <input type="date" value={ex.exam_date} onChange={e => updateExam(i, 'exam_date', e.target.value)} required />
              </div>
              <div className="form-group" style={{ maxWidth: 120 }}>
                <label className="form-label">Difficulty (1-5)</label>
                <select value={ex.difficulty} onChange={e => updateExam(i, 'difficulty', e.target.value)}>
                  {[1,2,3,4,5].map(d => <option key={d} value={d}>{d}</option>)}
                </select>
              </div>
              {exams.length > 1 && (
                <button type="button" className="btn-danger" onClick={() => removeExam(i)}>✕</button>
              )}
            </div>
          ))}
        </div>

        {/* ── Projects Panel ── */}
        <div className="panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div className="panel-title" style={{ margin: 0 }}>🛠 Projects</div>
            <button type="button" className="btn-secondary" onClick={addProject}>+ Add Project</button>
          </div>
          {projects.map((pr, i) => (
            <div className="form-row" key={i}>
              <div className="form-group">
                <label className="form-label">Project Name</label>
                <input value={pr.name} onChange={e => updateProject(i, 'name', e.target.value)}
                  placeholder="e.g. ML Research Paper" required />
              </div>
              <div className="form-group" style={{ maxWidth: 150 }}>
                <label className="form-label">Deadline</label>
                <input type="date" value={pr.deadline} onChange={e => updateProject(i, 'deadline', e.target.value)} required />
              </div>
              <div className="form-group" style={{ maxWidth: 140 }}>
                <label className="form-label">Est. Hours Total</label>
                <input type="number" min="1" max="200" value={pr.estimated_hours}
                  onChange={e => updateProject(i, 'estimated_hours', e.target.value)} required />
              </div>
              {projects.length > 1 && (
                <button type="button" className="btn-danger" onClick={() => removeProject(i)}>✕</button>
              )}
            </div>
          ))}
        </div>

        {/* ── Settings Row ── */}
        <div className="panel">
          <div className="panel-title">⚙️ Settings</div>
          <div className="form-row">
            <div className="form-group" style={{ maxWidth: 200 }}>
              <label className="form-label">Available Hours / Day</label>
              <input type="number" min="0.5" max="16" step="0.5" value={hoursDay}
                onChange={e => setHoursDay(e.target.value)} required />
            </div>
            <div className="form-group" style={{ maxWidth: 200 }}>
              <label className="form-label">Plan Start Date</label>
              <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Generating…' : '🚀 Generate Study Plan'}
          </button>
          <button type="button" className="btn-secondary" onClick={loadSample}>
            📋 Load Sample Data
          </button>
        </div>
      </form>

      {loading && <div style={{ marginTop: '2rem' }}><div className="spinner" /></div>}
      {result  && <StudyPlanResult result={result} />}
    </div>
  );
}

function StudyPlanResult({ result }) {
  const { schedule, priority_ranking, total_tasks, ai_recommendations, student_efficiency_score } = result;

  return (
    <div style={{ marginTop: '2rem' }}>
      {/* ── Stats Row ── */}
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-label">Tasks Scheduled</div>
          <div className="stat-value">{total_tasks}</div>
          <div className="stat-sub">exams + projects</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Plan Duration</div>
          <div className="stat-value">{schedule.length} days</div>
          <div className="stat-sub">active study days</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Efficiency Score</div>
          <div className="stat-value" style={{ color: scoreColor(student_efficiency_score) }}>
            {student_efficiency_score}
          </div>
          <div className="stat-sub">{scoreLabel(student_efficiency_score)}</div>
        </div>
      </div>

      {/* ── Priority Ranking ── */}
      <div className="section-title">🎯 Priority Ranking</div>
      <div className="card" style={{ marginBottom: '1.5rem', padding: '0.5rem 0' }}>
        <table className="priority-table">
          <thead>
            <tr>
              <th>#</th><th>Name</th><th>Type</th><th>Due Date</th>
              <th>Days Left</th><th>Urgency</th><th>Rec. Daily hrs</th>
            </tr>
          </thead>
          <tbody>
            {priority_ranking.map((item, i) => (
              <tr key={i}>
                <td style={{ color: '#6b7280' }}>{i + 1}</td>
                <td style={{ fontWeight: 600, color: '#e2e8f0' }}>{item.name}</td>
                <td><span className={`badge-${item.type === 'exam' ? 'high' : 'moderate'}`}>{item.type}</span></td>
                <td>{item.due_date}</td>
                <td style={{ color: item.days_remaining <= 3 ? '#f87171' : '#e2e8f0' }}>
                  {item.days_remaining}d
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <div style={{
                      width: `${Math.min(item.urgency_score * 2, 80)}px`,
                      height: 6, background: '#6366f1', borderRadius: 3,
                    }} />
                    <span style={{ fontSize: '0.78rem', color: '#9ca3af' }}>{item.urgency_score.toFixed(1)}</span>
                  </div>
                </td>
                <td>{item.recommended_daily_hours}h</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ── Daily Schedule ── */}
      <div className="section-title">📅 14-Day Study Schedule</div>
      <div className="schedule-list" style={{ marginBottom: '1.5rem' }}>
        {schedule.map((day, i) => (
          <div className="schedule-day" key={i}>
            <div>
              <div className="schedule-date">{day.date}</div>
              <div className="schedule-dow">{day.day_of_week}</div>
              <span className={`badge-${day.load_level}`} style={{ marginTop: '0.3rem', display: 'inline-block' }}>
                {day.load_level} · {day.total_hours}h
              </span>
            </div>
            <div className="schedule-tasks">
              {day.tasks.map((t, j) => <span key={j} className="task-pill">{t}</span>)}
            </div>
          </div>
        ))}
      </div>

      {/* ── AI Recommendations ── */}
      <div className="ai-box">
        <div className="ai-box-title">🤖 AI Recommendations</div>
        <p>{ai_recommendations}</p>
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
