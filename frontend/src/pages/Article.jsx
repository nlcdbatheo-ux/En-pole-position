import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import Loader from "../components/Loader";

function Article() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/news`)
      .then((res) => res.json())
      .then((data) => {
        const a = data.find((x) => x.id === parseInt(id));
        setArticle(a);
      });
  }, [id]);

  if (!article) return <Loader />;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold">{article.title}</h1>
      <p className="mt-4">{article.content}</p>
    </div>
  );
}

export default Article;
