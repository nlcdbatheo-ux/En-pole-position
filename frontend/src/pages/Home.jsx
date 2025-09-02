import { useEffect, useState } from "react";
import NewsCard from "../components/NewsCard";

function Home() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/news")
      .then((res) => res.json())
      .then((data) => setArticles(data));
  }, []);

  return (
    <div className="p-6 grid gap-4">
      {articles.map((a) => (
        <NewsCard key={a.id} article={a} />
      ))}
    </div>
  );
}

export default Home;
