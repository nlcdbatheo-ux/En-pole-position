import React, { useEffect, useState } from "react";
import NewsCard from "./components/NewsCard.jsx";

function App() {
  const [newsList, setNewsList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Remplace l'URL par celle de ton backend Render
    fetch("https://en-pole-position-1.onrender.com/api/news")
      .then((res) => res.json())
      .then((data) => {
        setNewsList(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du fetch des news:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p style={{ padding: "2rem" }}>Chargement des news…</p>;
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>En pole position 🏎️</h1>
      <p>Les dernières news de la Formule 1 :</p>
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        {newsList.map((news) => (
          <NewsCard key={news.id} title={news.title} summary={news.summary} />
        ))}
      </div>
    </div>
  );
}

export default App;
