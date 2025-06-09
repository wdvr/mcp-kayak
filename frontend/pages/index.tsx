import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const resp = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await resp.json();
    setResults(data.flights || []);
    setLoading(false);
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Flight Search</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="flights from SFO to LAX"
        />
        <button type="submit" disabled={loading}>
          Search
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {results.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Price</th>
              <th>Duration</th>
              <th>Class</th>
              <th>Depart</th>
              <th>Arrive</th>
              <th>From</th>
              <th>To</th>
              <th>Airline</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, i) => (
              <tr key={i}>
                <td>{r.price}</td>
                <td>{r.duration}</td>
                <td>{r.class}</td>
                <td>{r.depart_time}</td>
                <td>{r.arrive_time}</td>
                <td>{r.origin}</td>
                <td>{r.destination}</td>
                <td>{r.airline}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
