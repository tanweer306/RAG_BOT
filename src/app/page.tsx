"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import ChatInterface from "@/components/ChatInterface";
import FileUpload from "@/components/FileUpload";
import LanguageSelector from "@/components/LanguageSelector";
import DocumentList from "@/components/DocumentList";
import { getCurrentSession, getChatHistory, getDocuments } from "@/lib/api";
import { Message, Document } from "@/lib/types";

export default function Home() {
  const [sessionInfo, setSessionInfo] = useState<any>(null);
  const [language, setLanguage] = useState<string>("en");
  const [documents, setDocuments] = useState<Document[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Backend identifies user by IP automatically
      const session = await getCurrentSession();
      setSessionInfo(session);
      
      if (session.exists) {
        setLanguage(session.language || "en");
        
        // Load chat history
        try {
          const historyData = await getChatHistory();
          setMessages(historyData.history || []);
        } catch (e) {
          console.error("Failed to load history", e);
        }
        
        // Load documents
        try {
          const docsData = await getDocuments();
          setDocuments(docsData.documents || []);
        } catch (e) {
          console.error("Failed to load documents", e);
        }
      }
    } catch (error) {
      console.error("Error initializing session:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div
        className="flex items-center justify-center min-h-screen"
        data-oid="hwn376g"
      >
        <div className="text-center" data-oid="zh2aqx7">
          <div
            className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"
            data-oid="43:pyru"
          ></div>
          <p className="mt-4 text-gray-600" data-oid=".vgmi5p">
            Initializing session...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50 flex-col md:flex-row" data-oid="xv.pkbh">
      {/* Sidebar */}
      <div
        className="w-full md:w-80 bg-white border-b md:border-b-0 md:border-r border-gray-200 flex flex-col"
        data-oid="82qdqy2"
      >
        <div className="p-4 border-b border-gray-200" data-oid="isrs9-2">
          <h1 className="flex items-center gap-2 text-lg font-bold text-gray-800" data-oid="s2:tcc7">
            <Image src="/logo.png" alt="Docly logo" width={24} height={24} />
            <span>Docly</span>
          </h1>
           <h1 className="text-sm text-gray-800" data-oid="s2:tcc7">
             Your documents, answering back
          </h1>
          {sessionInfo?.exists && (
            <p className="text-sm text-gray-500 mt-1" data-oid="dkqg50w">
              {documents.length} docs • {messages.length} messages
            </p>
          )}
        </div>

        <div className="p-4 border-b border-gray-200" data-oid="jv9cut_">
          <LanguageSelector
            selectedLanguage={language}
            onLanguageChange={setLanguage}
            data-oid="w5wmvs-"
          />
        </div>

        <div className="p-4 border-b border-gray-200" data-oid="dvez._f">
          <FileUpload
            onUploadSuccess={(doc) => setDocuments([...documents, doc])}
            data-oid=".1q3qag"
          />
        </div>

        <div className="flex-1 overflow-y-auto" data-oid="enn4si7">
          <DocumentList
            documents={documents}
            onDocumentDeleted={(filename) =>
              setDocuments(documents.filter((d) => d.filename !== filename))
            }
            data-oid="_f3-y9:"
          />
        </div>

        <div
          className="p-4 border-t border-gray-200 text-xs text-gray-500"
          data-oid="qysvwt_"
        >
          <p data-oid="z1i1k-:">💡 Upload documents to start chatting</p>
          <p className="mt-1" data-oid="ccyq8nc">
            🎤 Use voice for audio queries
          </p>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white" data-oid="8x5vplh">
        <ChatInterface
          language={language}
          messages={messages}
          onMessagesUpdate={setMessages}
          data-oid="5oz3im5"
        />
      </div>
    </div>
  );
}
