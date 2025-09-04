
import { useEffect, useState } from "react";
import config from "./config";

export default function App() {
  const [tab, setTab] = useState("latest");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    const url =
      tab === "latest"
        ? `${config.API_BASE_URL}/api/validated`
        : `${config.API_BASE_URL}/api/history?days=7`;
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error("Impossible de charger les articles");
      const data = await r.json();
      setItems(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [tab]);

  const triggerRefresh = async () => {
    try {
      await fetch(`${config.API_BASE_URL}/api/refresh`, { method: "POST" });
      setTimeout(fetchData, 1500);
    } catch {}
  };

  return (
    <div className="min-h-screen px-4 pb-16 bg-gradient-to-b from-black via-gray-900 to-gray-950">
      <header className="max-w-6xl mx-auto pt-10 pb-6 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-red-500 drop-shadow-lg animate-pulse">
          🏎️ En Pôle Position
        </h1>
        <p className="text-gray-300 mt-2">Les infos F1 vérifiées par recoupement</p>

        <div className="mt-6 inline-flex rounded-2xl bg-gray-800/60 shadow">
          <button
            onClick={() => setTab("latest")}
            className={`px-5 py-2 rounded-2xl ${tab==="latest" ? "bg-red-600 text-white" : "text-gray-300"}`}
          >
            Dernières
          </button>
          <button
            onClick={() => setTab("history")}
            className={`px-5 py-2 rounded-2xl ${tab==="history" ? "bg-red-600 text-white" : "text-gray-300"}`}
          >
            Historique (7j)
          </button>
          <button
            onClick={triggerRefresh}
            className="px-5 py-2 rounded-2xl text-white bg-emerald-600 hover:bg-emerald-700"
          >
            Rafraîchir
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        {loading && <p className="text-gray-400 animate-pulse">Chargement...</p>}
        {error && <p className="text-red-400">{error}</p>}
        {!loading && !error && items.length === 0 && (
          <p className="text-gray-400">Aucune actualité pour le moment.</p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((it, idx) => (
            <article
              key={idx}
              className="bg-gray-900/70 rounded-2xl p-5 border border-white/5 hover:border-red-500/40 hover:shadow-xl transition transform hover:-translate-y-1 animate-fadeInUp"
            >
              <h2 className="text-xl font-semibold text-white">{it.title}</h2>
              <p className="text-gray-300 text-sm mt-2">{it.summary}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {it.sources?.map((s, i) => (
                  <a
                    key={i}
                    href={s}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs px-3 py-1 rounded-full bg-gray-800 hover:bg-gray-700"
                  >
                    Source {i+1}
                  </a>
                ))}
              </div>
              {it.created_at && (
                <p className="text-[11px] text-gray-500 mt-3">Publié: {new Date(it.created_at).toLocaleString()}</p>
              )}
            </article>
          ))}
        </div>
      </main>

      <footer className="max-w-6xl mx-auto mt-16 text-center text-gray-500 text-sm">
        © {new Date().getFullYear()} En Pôle Position — par recoupement multi-sources
      </footer>
    </div>
  );
}
