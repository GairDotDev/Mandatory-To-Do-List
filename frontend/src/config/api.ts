// API client configuration
// Uses API_BASE_URL from environment (set by infra team)
// Falls back to localhost for development
const API_BASE_URL = (import.meta.env.API_BASE_URL || import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000') as string;

export default API_BASE_URL;

