"use client";

import { useState, useRef } from "react";
import { Mic, MicOff } from "lucide-react";

interface Props {
  onRecordingComplete: (audioBlob: Blob) => void;
  disabled?: boolean;
}

export default function AudioRecorder({
  onRecordingComplete,
  disabled,
}: Props) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        // Use audio/webm as it's the standard browser recording format
        const audioBlob = new Blob(chunksRef.current, { type: "audio/webm" });
        if (audioBlob.size > 0) {
            onRecordingComplete(audioBlob);
        } else {
            console.error("Recorded audio blob is empty");
        }
        stream.getTracks().forEach((track) => track.stop());
      };

      // Request data every 200ms to ensure we capture short recordings too
      mediaRecorder.start(200);
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Could not access microphone. Please check permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <button
      type="button"
      onClick={toggleRecording}
      disabled={disabled}
      className={`p-2 rounded-lg transition-colors ${
        isRecording
          ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
          : "bg-gray-200 hover:bg-gray-300 text-gray-700"
      } disabled:opacity-50 disabled:cursor-not-allowed`}
      title={isRecording ? "Stop recording" : "Start recording"}
      data-oid="lmyn0_2"
    >
      {isRecording ? (
        <MicOff size={20} data-oid="4.l:p9m" />
      ) : (
        <Mic size={20} data-oid="1j3ovqm" />
      )}
    </button>
  );
}
