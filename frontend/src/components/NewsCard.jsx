import React from "react";

function NewsCard({ title, summary }) {
  return (
    <div style={{
      border: "1px solid #ccc",
      borderRadius: "8px",
      padding: "1rem",
      boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
      cursor: "pointer",
      transition: "transform 0.2s",
    }}
    onClick={() => alert(summary)} // Ici tu peux remplacer par une vraie page article
    >
      <h2>{title}</h2>
      <p>{summary}</p>
    </div>
  );
}

export default NewsCard;
