const BASE_URL = "http://localhost:8000";

export async function fetchNews() {
  const res = await fetch(`${BASE_URL}/news`);
  return await res.json();
}

export async function generateNews() {
  const res = await fetch(`${BASE_URL}/generate`, { method: "POST" });
  return await res.json();
}
