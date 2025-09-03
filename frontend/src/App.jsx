import React, { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function Header({ onRefresh }) {
  return (
    <div className="header">
      <div className="brand">
        <div className="logo" />
        <div>
          <h1 className="title">En Pole Position</h1>
          <p className="subtitle">Dernières actus F1</p>
        </div>
      </div>
      <div className="toolbar">
        <button className="btn" onClick={onRefresh}>🔄 Rafraîchir</button>
        <a
          className="btn primary"
          href="https://www.formula1.com/en/latest/all.html"
          target="_blank"
          rel="noreferrer"
        >
          F1 Officiel
        </a>
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

function ArticleCard({ a }) {
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
        </div>
      </div>
    </motion.div>
  );
}

export default function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  const sorted = useMemo(() => articles.slice(0, 60), [articles]);

  async function loadArticles() {
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`${API_BASE}/articles`, { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setArticles(dat
