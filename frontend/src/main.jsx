import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import "./style.css";

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    async function fetchArticles() {
      try {
        const res = await fetch("/api/articles"); // Assure-toi que le backend expose ce endpoint
        const data = await res.json();
        setArticles(data);
      } catch (err) {
        console.error("Erreur récupération articles:", err);
      }
    }

    fetchArticles();
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-red-600 text-white py-6 shadow-md">
        <h1 className="text-4xl font-extrabold text-center">En Pôle Position</h1>
        <p className="text-center text-lg mt-2">
          Les dernières infos F1 validées par IA
        </p>
      </header>

      <main className="max-w-5xl mx-auto mt-8 px-4">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {articles.length === 0 && (
            <p className="text-center text-gray-600 col-span-full">
              Chargement des articles...
            </p>
          )}
          {articles.map((article, index) => (
            <div
              key={index}
              className="card animate-fadeInUp"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <h2 className="text-xl font-bold mb-2 text-red-600">Résumé</h2>
              <p className="text-gray-700 mb-3">{article.summary}</p>
              <h3 className="font-semibold mt-2">Sources :</h3>
              <ul className="list-disc list-inside">
                {article.sources.map((src, idx) => (
                  <li key={idx}>
                    <a href={src} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                      {src}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </main>

      <footer className="bg-gray-200 text-gray-700 py-6 mt-12 text-center">
        © 2025 En Pôle Position | Sources multiples vérifiées par IA
      </footer>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
