import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
const API_URL = `${API_BASE}/admin`;

const getHeaders = () => {
  const token = localStorage.getItem("adminToken");
  return {
    Authorization: `Bearer ${token}`,
  };
};

export const adminApi = {
  login: (password: string) => {
    // Since we use simple password auth without a login endpoint in backend (just token verification)
    // We just return true if password is not empty, actual verification happens on data fetch
    return Promise.resolve(true);
  },

  getStats: async () => {
    const response = await axios.get(`${API_URL}/stats`, { headers: getHeaders() });
    return response.data;
  },

  getSessions: async (page = 1, limit = 20, status?: string) => {
    const response = await axios.get(`${API_URL}/sessions`, {
      params: { page, limit, status },
      headers: getHeaders(),
    });
    return response.data;
  },

  getSessionDetails: async (sessionId: string) => {
    const response = await axios.get(`${API_URL}/sessions/${sessionId}`, {
      headers: getHeaders(),
    });
    return response.data;
  },

  deleteSession: async (sessionId: string) => {
    const response = await axios.delete(`${API_URL}/sessions/${sessionId}`, {
      headers: getHeaders(),
    });
    return response.data;
  },

  getDocuments: async (page = 1, limit = 20, expired = false) => {
    const response = await axios.get(`${API_URL}/documents`, {
      params: { page, limit, expired },
      headers: getHeaders(),
    });
    return response.data;
  },

  deleteDocument: async (documentId: string) => {
    const response = await axios.delete(`${API_URL}/documents/${documentId}`, {
      headers: getHeaders(),
    });
    return response.data;
  },

  getAnalytics: async (days = 7) => {
    const response = await axios.get(`${API_URL}/analytics`, {
      params: { days },
      headers: getHeaders(),
    });
    return response.data;
  },

  runCleanup: async () => {
    const response = await axios.post(`${API_URL}/cleanup`, {}, {
      headers: getHeaders(),
    });
    return response.data;
  },
};
