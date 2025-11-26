export interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  timestamp: string;
  isAudio?: boolean;
}

export interface Document {
  filename: string;
  url: string;
  chunks: number;
  uploaded_at: string;
}

export interface Session {
  session_id: string;
  language: string;
  documents_count: number;
  messages_count: number;
  created_at: string;
  last_active: string;
}

export const LANGUAGES = [
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "es", name: "Español", flag: "🇪🇸" },
  { code: "fr", name: "Français", flag: "🇫🇷" },
  { code: "de", name: "Deutsch", flag: "🇩🇪" },
  { code: "ar", name: "العربية", flag: "🇸🇦" },
  { code: "ur", name: "اردو", flag: "🇵🇰" },
  { code: "zh", name: "中文", flag: "🇨🇳" },
];
