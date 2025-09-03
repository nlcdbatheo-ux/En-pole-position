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
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col items-center p-6">
      <h1 className="text-5xl font-extrabold text-red-500 drop-shadow-lg animate-pulse mb-8">
        🏎️ En Pôle Position
      </h1>

      {loading && (
        <p className="text-gray-400 animate-fadeInUp">Chargement des articles...</p>
      )}
      {error && <p className="text-red-400 animate-fadeInUp">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-7xl mt-6">
        {articles.map((article, idx) => (
          <div
            key={idx}
            className="bg-gray-800 rounded-3xl p-6 shadow-lg hover:shadow-red-500/40 transition transform hover:-translate-y-3 animate-fadeInUp"
          >
            <h2 className="text-2xl font-bold text-red-400 mb-3">{article.summary ? article.summary.slice(0, 60) + "…" : "F1 News"}</h2>
            <p className="text-gray-300 text-sm mb-4">{article.summary || "Pas de résumé disponible."}</p>
            <div className="flex justify-between items-center">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-white bg-red-600 px-4 py-2 rounded-2xl shadow hover:bg-red-700 transition"
              >
                Lire l’article
              </a>
              <span className="text-gray-400 text-xs">{article.sources ? article.sources.length + " sources" : ""}</span>
            </div>
          </div>
        ))}
      </div>

      {!loading && !error && articles.length === 0 && (
        <p className="text-gray-400 mt-12 animate-fadeInUp">
          Aucun article validé pour le moment.
        </p>
      )}
    </div>
  );
}

export default App;
