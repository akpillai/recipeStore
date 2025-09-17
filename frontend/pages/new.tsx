import { useState } from 'react';
const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function NewRecipe() {
  const [name, setName] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [ingredients, setIngredients] = useState('');
  const [steps, setSteps] = useState('');
  const [tags, setTags] = useState('');
  const [status, setStatus] = useState('');

  const submit = async () => {
    setStatus('Saving...');
    const payload = {
      name,
      cuisine: cuisine || null,
      ingredients: ingredients ? ingredients.split('\n').map(s=>s.trim()).filter(Boolean) : null,
      steps: steps ? steps.split('\n').map(s=>s.trim()).filter(Boolean) : null,
      tags: tags ? tags.split(',').map(s=>s.trim()).filter(Boolean) : null
    };
    const res = await fetch(`${API}/recipes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      setStatus(`Error: ${err.detail || res.status}`);
      return;
    }
    setStatus('Saved!');
    setName(''); setCuisine(''); setIngredients(''); setSteps(''); setTags('');
  };

  return (
    <main style={{ maxWidth: 800, margin: '2rem auto', padding: '0 1rem' }}>
      <h1>➕ Add a Recipe</h1>
      <label>Name<br/><input value={name} onChange={e=>setName(e.target.value)} style={{width:'100%', padding:8}}/></label>
      <label>Cuisine (optional)<br/><input value={cuisine} onChange={e=>setCuisine(e.target.value)} style={{width:'100%', padding:8}}/></label>
      <label>Ingredients (one per line)<br/><textarea value={ingredients} onChange={e=>setIngredients(e.target.value)} rows={6} style={{width:'100%', padding:8}}/></label>
      <label>Steps (one per line)<br/><textarea value={steps} onChange={e=>setSteps(e.target.value)} rows={8} style={{width:'100%', padding:8}}/></label>
      <label>Tags (comma-separated)<br/><input value={tags} onChange={e=>setTags(e.target.value)} style={{width:'100%', padding:8}}/></label>
      <div style={{marginTop:12}}><button onClick={submit}>Save</button> <span style={{marginLeft:8}}>{status}</span></div>
      <p style={{marginTop:16}}><a href="/">← Back</a></p>
    </main>
  );
}
