"use client";

import { LANGUAGES } from "@/lib/types";
import { updateLanguage } from "@/lib/api";

interface Props {
  selectedLanguage: string;
  onLanguageChange: (language: string) => void;
}

export default function LanguageSelector({
  selectedLanguage,
  onLanguageChange,
}: Props) {
  const handleChange = async (language: string) => {
    try {
      await updateLanguage(language);
      onLanguageChange(language);
    } catch (error) {
      console.error("Error updating language:", error);
    }
  };

  return (
    <div data-oid="xp3ibvx">
      <label
        className="block text-sm font-medium text-gray-700 mb-2"
        data-oid="p65cc8u"
      >
        Language
      </label>
      <select
        value={selectedLanguage}
        onChange={(e) => handleChange(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        data-oid="fiivglo"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code} data-oid="q12jw5s">
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
}
