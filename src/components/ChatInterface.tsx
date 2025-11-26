"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Plus } from "lucide-react";
import { sendMessage, sendAudioMessage } from "@/lib/api";
import { Message as MessageType } from "@/lib/types";
import Message from "./Message";
import AudioRecorder from "./AudioRecorder";

interface Props {
  language: string;
  messages: MessageType[];
  onMessagesUpdate: (messages: MessageType[] | ((prev: MessageType[]) => MessageType[])) => void;
}

export default function ChatInterface({
  language,
  messages,
  onMessagesUpdate,
}: Props) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: MessageType = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    // Optimistically add user message
    onMessagesUpdate([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await sendMessage(input, language);

      const assistantMessage: MessageType = {
        role: "assistant",
        content: response.response,
        sources: response.sources,
        timestamp: new Date().toISOString(),
      };

      onMessagesUpdate((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error("Error sending message:", error);
      
      onMessagesUpdate((prev) => {
          return [...prev, {
              role: "assistant",
              content: "Sorry, I encountered an error. Please try again.",
              timestamp: new Date().toISOString()
          }];
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAudioRecording = async (audioBlob: Blob) => {
    setLoading(true);

    const userMessage: MessageType = {
      role: "user",
      content: "🎤 Audio message",
      timestamp: new Date().toISOString(),
      isAudio: true,
    };

    onMessagesUpdate([...messages, userMessage]);

    try {
      const audioResponse = await sendAudioMessage(
        audioBlob,
        language,
      );

      // Create audio URL for playback
      const audioUrl = URL.createObjectURL(audioResponse);

      const assistantMessage: MessageType = {
        role: "assistant",
        content: audioUrl,
        timestamp: new Date().toISOString(),
        isAudio: true,
      };

      onMessagesUpdate((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error("Error sending audio:", error);

      const errorMessage: MessageType = {
        role: "assistant",
        content: "Sorry, I couldn't process your audio. Please try again.",
        timestamp: new Date().toISOString(),
      };
      onMessagesUpdate((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const inputForm = (
    <form
      onSubmit={handleSubmit}
      className={`flex items-center w-full bg-white transition-all duration-300 ${
        messages.length === 0
          ? "rounded-full border border-gray-200 shadow-lg px-6 py-4"
          : "rounded-lg border border-gray-300 px-4 py-2"
      }`}
    >
      {messages.length === 0 && (
        <Plus className="text-gray-400 mr-3 h-5 w-5" />
      )}
      
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={messages.length === 0 ? "Ask anything..." : "Ask a question about your documents..."}
        className="flex-1 bg-transparent focus:outline-none text-gray-700 placeholder-gray-400"
        disabled={loading}
        autoFocus={messages.length === 0}
      />

      <div className="flex items-center space-x-2 ml-2">
        <AudioRecorder
          onRecordingComplete={handleAudioRecording}
          disabled={loading}
        />

        <button
          type="submit"
          disabled={!input.trim() || loading}
          className={`p-2 rounded-full transition-colors ${
             !input.trim() || loading 
             ? "text-gray-300 cursor-not-allowed" 
             : "text-blue-600 hover:bg-blue-50"
          }`}
        >
          <Send size={20} />
        </button>
      </div>
    </form>
  );

  return (
    <div className="flex flex-col h-full relative" data-oid="_tq6gsw">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 scroll-smooth" data-oid="pv6-:2o">
        {messages.length > 0 ? (
          <>
            {messages.map((msg, idx) => (
              <Message key={idx} message={msg} data-oid="iuqz2kz" />
            ))}
            {loading && (
              <div
                className="flex items-center space-x-2 text-gray-500"
                data-oid="6xq430x"
              >
                <div
                  className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"
                  data-oid="p7:o.ku"
                ></div>
                <span data-oid="xwyq_ly">Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} data-oid="bm6pgs2" />
          </>
        ) : (
          // Empty state center container
          <div className="h-full flex flex-col items-center justify-center -mt-20">
             <h1 className="text-3xl font-light text-gray-800 mb-8 animate-fade-in">
               Ready when you are.
             </h1>
             <div className="w-full max-w-2xl px-4">
                {inputForm}
             </div>
             <p className="text-sm text-gray-400 mt-4">
                Ask about your uploaded documents
             </p>
          </div>
        )}
      </div>

      {/* Bottom Input Area (Only visible when messages exist) */}
      {messages.length > 0 && (
        <div className="border-t border-gray-200 p-4 bg-white" data-oid="omuwem5">
          <div className="max-w-4xl mx-auto">
            {inputForm}
          </div>
        </div>
      )}
    </div>
  );
}
