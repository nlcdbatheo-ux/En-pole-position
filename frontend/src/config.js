
const isRender = typeof window !== "undefined" && window.location.hostname.endsWith("onrender.com");
const API_BASE_URL = isRender ? "" : "http://localhost:8000";
export default { API_BASE_URL };
