import axios from "axios";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Session APIs
export const getCurrentSession = async () => {
  const { data } = await api.get("/session/current");
  return data;
};

export const updateLanguage = async (language: string) => {
  const { data } = await api.post("/session/language", {
    language,
  });
  return data;
};

// Document APIs
export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const getDocuments = async () => {
  const { data } = await api.get("/documents");
  return data;
};

export const deleteDocument = async (filename: string) => {
  const { data } = await api.delete(`/documents/${filename}`);
  return data;
};

// Chat APIs
export const sendMessage = async (query: string, language: string) => {
  const { data } = await api.post("/chat", {
    query,
    language,
  });
  return data;
};

export const sendAudioMessage = async (
  audioBlob: Blob,
  language: string,
) => {
  const formData = new FormData();
  formData.append("audio", audioBlob, "audio.wav");

  const { data } = await api.post(
    `/chat/audio?language=${language}`,
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
      responseType: "blob",
    },
  );
  return data;
};

export const getChatHistory = async () => {
  const { data } = await api.get('/chat/history?limit=50');
  return data;
};
