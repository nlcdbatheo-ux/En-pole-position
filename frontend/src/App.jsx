import { useEffect, useState } from "react";
import config from "./config";

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const res = await fetch(`${config.API_BASE_URL}/validated`);
        if (!res.ok) throw new Error("Impossible de charger les articles");
        const data = await res.json();
        setArticles(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center p-6">
      <h1 className="text-4xl font-extrabold text-red-500 drop-shadow-lg animate-pulse mb-6">
        🏎️ En Pôle Position
      </h1>

      {loading && <p className="text-gray-400 animate-pulse">Chargement des articles...</p>}
      {error && <p className="text-red-400">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
        {articles.map((article, idx) => (
          <div
            key={idx}
            className="bg-gray-800 rounded-2xl p-5 shadow-lg hover:shadow-red-500/30 transition duration-300 transform hover:-translate-y-2"
          >
            <h2 className="text-xl font-semibold text-red-400 mb-2">
              {article.title}
            </h2>
            <p className="text-gray-300 text-sm mb-4">
              {article.summary || "Pas de résumé disponible."}
            </p>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-white bg-red-600 px-4 py-2 rounded-xl shadow hover:bg-red-700 transition"
            >
              Lire l’article
            </a>
          </div>
        ))}
      </div>

      {articles.length === 0 && !loading && !error && (
        <p className="text-gray-400 mt-10">Aucun article validé pour le moment.</p>
      )}
    </div>
  );
}

export default App;
