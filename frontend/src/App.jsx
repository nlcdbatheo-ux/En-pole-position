import React, { useEffect, useState } from "react";

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchArticles() {
      try {
        // ⚠️ Remplace l’URL par ton backend Render (ex: https://en-pole-backend.onrender.com)
        const res = await fetch("http://localhost:8000/articles");
        const data = await res.json();
        setArticles(data.articles);
      } catch (err) {
        console.error("Erreur lors du fetch :", err);
      } finally {
        setLoading(false);
      }
    }

    fetchArticles();
  }, []);

  if (loading) {
    return <p>Chargement des articles...</p>;
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>🏎️ En Pole Position</h1>
      <h2>Dernières actualités F1</h2>
      <ul>
        {articles.map((a, idx) => (
          <li key={idx} style={{ margin: "1rem 0" }}>
            <a href={a.url} target="_blank" rel="noopener noreferrer">
              {a.title}
            </a>{" "}
            <small>({a.source})</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
