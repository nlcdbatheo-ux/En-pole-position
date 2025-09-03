import React, { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

// 1) Configure l'URL du backend ici (priorité à la variable d'env Vite sur Render)
const API_BASE =
  import.meta.env.VITE_API_BASE_URL // à définir côté Render (Static Site) → URL de ton backend
  || "http://localhost:8000";       // fallback local

function Header({ onRefresh }) {
  return (
    <div className="header">
      <div className="brand">
        <div className="logo" />
        <div>
          <h1 className="title">En Pole Position</h1>
          <p className="subtitle">Dernières actus F1 • résumées par IA</p>
        </div>
      </div>
      <div className="toolbar">
        <button className="btn" onClick={onRefresh}>🔄 Rafraîchir</button>
        <a className="btn primary" href="https://www.formula1.com/en/latest/all.html" target="_blank" rel="noreferrer">F1 Officiel</a>
      </div>
    </div>
  );
}

function SkeletonGrid() {
  return (
    <div className="grid" aria-hidden="true">
      {Array.from({ length: 9 }).map((_, i) => (
        <div className="skeleton" key={i} />
      ))}
    </div>
  );
}

function ArticleCard({ a, onSummarize, summary }) {
  return (
    <motion.div
      className="card"
      initial={{ opacity: 0, y: 10, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.20, ease: "easeOut" }}
      onMouseMove={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        const mx = ((e.clientX - r.left) / r.width) * 100;
        e.currentTarget.style.setProperty("--mx", `${mx}%`);
      }}
    >
      <div className="card-header">
        <div>
          <h3 className="card-title">
            <a href={a.url} target="_blank" rel="noreferrer" style={{ color: "inherit", textDecoration: "none" }}>
              {a.title}
            </a>
          </h3>
          <p className="card-meta">Source : {a.source}</p>
        </div>
        <div className="actions">
          <span className="badge">Actu</span>
          <button className="btn" onClick={() => onSummarize(a)}>✨ Résumer (IA)</button>
        </div>
      </div>

      <AnimatePresence mode="popLayout">
        {summary && (
          <motion.div
            className="summary"
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 6 }}
            transition={{ duration: 0.18 }}
          >
            {summary}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [summaries, setSummaries] = useState({});
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  const sorted = useMemo(() => articles.slice(0, 60), [articles]); // limite d’affichage

  async function loadArticles() {
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`${API_BASE}/articles`, { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setArticles(data.articles || []);
    } catch (e) {
      setError("Impossible de charger les articles. Vérifie l'URL du backend (VITE_API_BASE_URL).");
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function refreshScrape() {
    setRefreshing(true);
    try {
      await fetch(`${API_BASE}/refresh`, { method: "POST" });
      await loadArticles();
    } catch (e) {
      console.error(e);
    } finally {
      setRefreshing(false);
    }
  }

  async function summarize(a) {
    try {
      const r = await fetch(`${API_BASE}/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: a.url, title: a.title })
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setSummaries((prev) => ({ ...prev, [a.url]: data.summary }));
    } catch (e) {
      setSummaries((prev) => ({ ...prev, [a.url]: "❌ Erreur IA (quota ? clé ?). Réessaie plus tard." }));
      console.error(e);
    }
  }

  useEffect(() => { loadArticles(); }, []);

  return (
    <div className="container">
      <Header onRefresh={refreshScrape} />

      {error && (
        <div className="summary" style={{ borderColor: "#5b1b1b", background: "linear-gradient(180deg,#1a1010,#120b0b)" }}>
          {error}
        </div>
      )}

      {refreshing && (
        <div className="summary">Rafraîchissement des sources…</div>
      )}

      {loading ? (
        <SkeletonGrid />
      ) : (
        <div className="grid">
          {sorted.map((a, i) => (
            <ArticleCard
              key={`${a.url}-${i}`}
              a={a}
              onSummarize={summarize}
              summary={summaries[a.url]}
            />
          ))}
        </div>
      )}
    </div>
  );
}
