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
    <div className="min-h-screen bg-gray-950 text-white p-6 flex flex-col items-center">
      <h1 className="text-5xl font-extrabold text-red-500 drop-shadow-lg animate-pulse mb-8">
        🏎️ En Pôle Position
      </h1>

      {loading && (
        <p className="text-gray-400 animate-pulse text-lg">Chargement des articles...</p>
      )}
      {error && <p className="text-red-400 text-lg">{error}</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-7xl">
        {articles.length > 0 &&
          articles.map((article, idx) => (
            <div
              key={idx}
              className="bg-gray-800 rounded-2xl p-6 shadow-lg transform transition duration-300 hover:-translate-y-2 hover:shadow-red-500/50 animate-fadeInUp"
            >
              <h2 className="text-xl font-semibold text-red-400 mb-3">{article.title}</h2>
              <p className="text-gray-300 mb-4">
                {article.summary || "Pas de résumé disponible."}
              </p>
              <div className="flex justify-between items-center">
                <a
                  href={article.sources ? article.sources[0] : "#"}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-white bg-red-600 px-4 py-2 rounded-xl shadow hover:bg-red-700 transition"
                >
                  Lire l’article
                </a>
                {article.sources && article.sources.length > 1 && (
                  <span className="text-gray-400 text-xs ml-2">
                    {article.sources.length} sources
                  </span>
                )}
              </div>
            </div>
          ))}
      </div>

      {!loading && articles.length === 0 && !error && (
        <p className="text-gray-400 mt-10 text-lg">
          Aucun article validé pour le moment.
        </p>
      )}
    </div>
  );
}

export default App;
