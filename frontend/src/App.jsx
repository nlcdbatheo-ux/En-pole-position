import { useEffect, useState } from "react";
import { VITE_API_BASE_URL } from "./config";

export default function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch(`${VITE_API_BASE_URL}/articles`)
      .then(res => res.json())
      .then(data => setArticles(data))
      .catch(err => console.error("Impossible de charger les articles:", err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-6 animate-bounce">En Pôle Position</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {articles.map(article => (
          <a
            key={article.id}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="p-4 bg-white rounded shadow hover:shadow-lg transition transform hover:-translate-y-1"
          >
            <h2 className="text-xl font-semibold">{article.title}</h2>
            <p className="text-gray-600 text-sm">{new Date(article.created_at).toLocaleString()}</p>
          </a>
        ))}
      </div>
    </div>
  );
}
