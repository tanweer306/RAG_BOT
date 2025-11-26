"use client";

import { useState } from "react";
import { FileText, Trash2 } from "lucide-react";
import { deleteDocument } from "@/lib/api";
import { Document } from "@/lib/types";

interface Props {
  documents: Document[];
  onDocumentDeleted: (filename: string) => void;
}

export default function DocumentList({
  documents,
  onDocumentDeleted,
}: Props) {
  const [loading, setLoading] = useState(false);

  const handleDelete = async (filename: string) => {
    if (!confirm(`Delete ${filename}?`)) return;

    setLoading(true);
    try {
      await deleteDocument(filename);
      onDocumentDeleted(filename);
    } catch (error) {
      console.error("Error deleting document:", error);
      alert("Failed to delete document");
    } finally {
      setLoading(false);
    }
  };

  if (documents.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 text-sm" data-oid="f5h34f9">
        No documents uploaded yet
      </div>
    );
  }

  return (
    <div className="p-4" data-oid="x857ol9">
      <h3
        className="text-sm font-semibold text-gray-700 mb-3"
        data-oid="nfq:p4f"
      >
        Documents ({documents.length})
      </h3>
      <div className="space-y-2" data-oid="fzj9p9l">
        {documents.map((doc) => (
          <div
            key={doc.filename}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            data-oid="52-1sya"
          >
            <div
              className="flex items-center space-x-2 flex-1 min-w-0"
              data-oid="h2ad9hp"
            >
              <FileText
                size={16}
                className="text-blue-600 flex-shrink-0"
                data-oid="c1pegls"
              />

              <div className="flex-1 min-w-0" data-oid="-e_1nwk">
                <p
                  className="text-sm font-medium text-gray-800 truncate"
                  data-oid="rgwtkzq"
                >
                  {doc.filename}
                </p>
                <p className="text-xs text-gray-500" data-oid="jp_cj9_">
                  {doc.chunks} chunks
                </p>
              </div>
            </div>
            <button
              onClick={() => handleDelete(doc.filename)}
              disabled={loading}
              className="p-1 text-red-600 hover:bg-red-50 rounded transition-colors disabled:opacity-50"
              data-oid="2q9_ol9"
            >
              <Trash2 size={16} data-oid="090a711" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
