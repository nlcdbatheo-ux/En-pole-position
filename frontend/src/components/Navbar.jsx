import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between">
      <Link to="/" className="text-2xl font-bold">En pole position 🏎️</Link>
    </nav>
  );
}

export default Navbar;
