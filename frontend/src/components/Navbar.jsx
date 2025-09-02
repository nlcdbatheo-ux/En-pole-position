import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={{ padding: "1rem", background: "#111", color: "white" }}>
      <Link to="/" style={{ color: "white", fontWeight: "bold", fontSize: "1.5rem" }}>
        En pole position 🏎️
      </Link>
    </nav>
  );
}

export default Navbar;
