"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, CheckCircle, AlertCircle } from "lucide-react";
import { uploadDocument } from "@/lib/api";

interface Props {
  onUploadSuccess: (document: any) => void;
}

export default function FileUpload({ onUploadSuccess }: Props) {
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [message, setMessage] = useState("");
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);

  const onDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const handleUpload = async (file: File) => {
      if (!file) return;

      // Client-side file size check (50MB)
      const fileSizeMB = file.size / (1024 * 1024);
      if (fileSizeMB > 50) {
        setStatus("error");
        setMessage(`File too large (${fileSizeMB.toFixed(2)}MB). Maximum: 50MB`);
        return;
      }

      setUploading(true);
      setStatus("idle");
      setMessage("");
      setProgress(0);

      // Simulated progress interval
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) return prev;
          return prev + 5;
        });
      }, 500);

      // Status message rotation
      const statusTimeout1 = setTimeout(() => setMessage("Uploading to cloud..."), 1000);
      const statusTimeout2 = setTimeout(() => setMessage("Extracting text..."), 3000);
      const statusTimeout3 = setTimeout(() => setMessage("Creating embeddings..."), 6000);

      try {
        const response = await uploadDocument(file);
        
        clearInterval(progressInterval);
        setProgress(100);
        setMessage("Finalizing...");
        
        const newDoc: any = {
          filename: response.filename,
          chunks: response.chunks_created,
          url: response.file_url,
          uploaded_at: new Date().toISOString()
        };
        
        setStatus("success");
        setMessage(`${response.filename} uploaded successfully!`);
        onUploadSuccess(newDoc);
        
        // Show limit warning if applicable
        if (response.documents_remaining === 0) {
           setTimeout(() => setMessage("Document limit reached. Delete to upload another."), 2000);
        }

      } catch (err: any) {
        console.error("Upload failed:", err);
        clearInterval(progressInterval);
        setStatus("error");
        const errorMsg = err.response?.data?.detail || err.message || "Upload failed";
        setMessage(errorMsg);
        setProgress(0);
      } finally {
        setUploading(false);
        clearTimeout(statusTimeout1);
        clearTimeout(statusTimeout2);
        clearTimeout(statusTimeout3);
      }
    };

    const file = acceptedFiles[0];
    handleUpload(file);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        [".docx"],
      "text/plain": [".txt"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
      "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        [".pptx"],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false,
  });

  return (
    <div>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          isDragActive
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300 hover:border-gray-400"
        } ${uploading ? "opacity-50 cursor-not-allowed" : ""}`}
      >
        <input {...getInputProps()} disabled={uploading} />
        <Upload className="mx-auto h-8 w-8 text-gray-400" />
        <p className="mt-2 text-sm text-gray-600">
          {isDragActive ? "Drop file here" : "Drag & drop or click to upload"}
        </p>
        <p className="mt-1 text-xs text-gray-500">
          PDF, DOCX, TXT, XLSX, PPTX (max 50MB)
        </p>
        <p className="mt-1 text-xs font-semibold text-orange-600">
          Limit: 1 document per user
        </p>
      </div>

      {uploading && (
        <div className="mt-4 space-y-2">
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-500" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
            <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600"></div>
            <span>{message || "Processing..."}</span>
          </div>
        </div>
      )}

      {status === "success" && (
        <div className="mt-3 flex items-center space-x-2 text-sm text-green-600">
          <CheckCircle size={16} />
          <span>{message}</span>
        </div>
      )}

      {status === "error" && (
        <div className="mt-3 flex items-center space-x-2 text-sm text-red-600">
          <AlertCircle size={16} />
          <span>{message}</span>
        </div>
      )}
    </div>
  );
}
