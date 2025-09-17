import { useState } from 'react';
const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function AskAI() {
  const [recipeName, setRecipeName] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [status, setStatus] = useState('');

  const submit = async () => {
    setStatus('Thinking...');
    setAnswer('');
    const payload: any = {};
    if (recipeName) payload.recipe_name = recipeName;
    if (question) payload.question = question;
    const res = await fetch(`${API}/ai/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    setStatus('');
    setAnswer(data.answer || JSON.stringify(data));
  };

  return (
    <main style={{ maxWidth: 800, margin: '2rem auto', padding: '0 1rem' }}>
      <h1>🤖 Ask the Kitchen AI</h1>
      <label>Recipe Name (optional)<br/><input value={recipeName} onChange={e=>setRecipeName(e.target.value)} style={{width:'100%', padding:8}}/></label>
      <label>Or a Question<br/><input value={question} onChange={e=>setQuestion(e.target.value)} style={{width:'100%', padding:8}}/></label>
      <div style={{marginTop:12}}><button onClick={submit}>Ask</button> <span style={{marginLeft:8}}>{status}</span></div>
      {answer && <pre style={{whiteSpace:'pre-wrap', background:'#f7f7f7', padding:12, borderRadius:8, marginTop:12}}>{answer}</pre>}
      <p style={{marginTop:16}}><a href="/">← Back</a></p>
    </main>
  );
}
