import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import Loader from "../components/Loader";

function Article() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/news")
      .then((res) => res.json())
      .then((data) => {
        const a = data.find((x) => x.id === parseInt(id));
        setArticle(a);
      });
  }, [id]);

  if (!article) return <Loader />;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>{article.title}</h1>
      <p>{article.content}</p>
    </div>
  );
}

export default Article;
