import { Link } from "react-router-dom";

function NewsCard({ article }) {
  return (
    <div className="p-4 bg-white shadow rounded-2xl">
      <h2 className="text-xl font-bold">{article.title}</h2>
      <p>{article.content.slice(0, 120)}...</p>
      <Link to={`/article/${article.id}`} className="text-blue-600">
        Lire plus →
      </Link>
    </div>
  );
}

export default NewsCard;
