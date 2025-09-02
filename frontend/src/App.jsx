import React from "react";
import NewsCard from "./components/NewsCard.jsx";

function App() {
  // Exemple de données statiques pour tester l'affichage
  const newsList = [
    { id: 1, title: "Pole position: Verstappen", summary: "Verstappen domine les essais libres." },
    { id: 2, title: "Hamilton en difficulté", summary: "Hamilton rencontre des problèmes techniques." },
    { id: 3, title: "Leclerc sur le podium", summary: "Leclerc termine 3ème lors de la première session." }
  ];

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
