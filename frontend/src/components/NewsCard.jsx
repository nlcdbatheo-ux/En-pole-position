import { Link } from "react-router-dom";

function NewsCard({ article }) {
  return (
    <div style={{ padding: "1rem", background: "white", marginBottom: "1rem", borderRadius: "12px" }}>
      <h2>{article.title}</h2>
      <p>{article.content.slice(0, 120)}...</p>
      <Link to={`/article/${article.id}`}>Lire plus →</Link>
    </div>
  );
}

export default NewsCard;
