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
      <header className="w-full max-w-6xl mb-8 text-center">
        <h1 className="text-5xl font-extrabold text-red-500 drop-shadow-lg animate-fadeInUp">
          🏎️ En Pôle Position
        </h1>
        <p className="text-gray-300 mt-2 animate-fadeInUp">
          Les dernières infos F1 validées par IA
        </p>
      </header>

      {loading && <p className="text-gray-400 animate-pulse">Chargement des articles...</p>}
      {error && <p className="text-red-400">{error}</p>}

      <main className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
        {articles.map((article, idx) => (
          <div
            key={idx}
            className="bg-gray-800 rounded-2xl p-6 shadow-lg hover:shadow-red-500/40 transition duration-300 transform hover:-translate-y-2 animate-fadeInUp"
          >
            <h2 className="text-xl font-semibold text-red-400 mb-3">{article.title}</h2>
            <p className="text-gray-300 text-sm mb-5">
              {article.summary || "Pas de résumé disponible."}
            </p>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-white bg-red-600 px-5 py-2 rounded-xl shadow hover:bg-red-700 transition"
            >
              Lire l’article
            </a>
          </div>
        ))}
      </main>

      {!loading && !error && articles.length === 0 && (
        <p className="text-gray-400 mt-10">Aucun article validé pour le moment.</p>
      )}

      <footer className="w-full mt-12 text-center text-gray-500 text-sm">
        &copy; {new Date().getFullYear()} En Pôle Position
      </footer>
    </div>
  );
}

export default App;

