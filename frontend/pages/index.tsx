import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function Home() {
  const [q, setQ] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const search = async () => {
    const url = new URL('/recipes', API);
    if (q) url.searchParams.set('q', q);
    const res = await fetch(url.toString());
    const data = await res.json();
    setResults(data);
  };

  useEffect(() => { search(); }, []);

  return (
    <main style={{ maxWidth: 800, margin: '2rem auto', padding: '0 1rem' }}>
      <h1>🍳 Recipe Finder</h1>
      <div style={{ display: 'flex', gap: 8 }}>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search by name or ingredient..." style={{ flex: 1, padding: 8 }} />
        <button onClick={search}>Search</button>
      </div>
      <ul>
        {results.map((r) => (
          <li key={r.id} style={{ margin: '1rem 0', padding: '1rem', border: '1px solid #ddd', borderRadius: 8 }}>
            <strong>{r.name}</strong> {r.cuisine ? `• ${r.cuisine}` : ''}
            {r.ingredients && <div><em>Ingredients:</em> {r.ingredients.join(', ')}</div>}
            {r.steps && <div><em>Steps:</em> <ol>{r.steps.map((s: string, i: number)=><li key={i}>{s}</li>)}</ol></div>}
          </li>
        ))}
      </ul>
      <p><a href="/new">➕ Add a Recipe</a> &nbsp; | &nbsp; <a href="/ask">🤖 Ask AI</a></p>
    </main>
  );
}
