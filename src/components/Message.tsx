import { Message as MessageType } from "@/lib/types";
import { User } from "lucide-react";
import Image from "next/image";

interface Props {
  message: MessageType;
}

export default function Message({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
      data-oid="w9m7ysp"
    >
      <div
        className={`flex space-x-2 max-w-2xl ${isUser ? "flex-row-reverse space-x-reverse" : ""}`}
        data-oid="24_.nxs"
      >
        <div
          className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? "bg-gray-300" : "bg-white"
          }`}
          data-oid="wcf-17p"
        >
          {isUser ? (
            <User size={16} className="text-black" data-oid="ss-53gp" />
          ) : (
            <Image
              src="/favicon.png"
              alt="Assistant"
              width={16}
              height={16}
              className="text-black"
              data-oid="1gdt9-p"
            />
          )}
        </div>

        <div
          className={`px-4 py-2 rounded-lg ${
            isUser ? "bg-gray-100 text-black" : "bg-white text-gray-800"
          }`}
          data-oid="y42yl-1"
        >
          {message.isAudio ? (
            <audio
              controls
              src={message.content}
              className="max-w-sm"
              data-oid="2yr_o0w"
            />
          ) : (
            <p className="whitespace-pre-wrap" data-oid="drg2zeg">
              {message.content}
            </p>
          )}

          {message.sources && message.sources.length > 0 && (
            <div
              className="mt-2 pt-2 border-t border-gray-300 text-sm"
              data-oid="3vu:_7i"
            >
              <p className="font-semibold" data-oid="1q3z:m6">
                Sources:
              </p>
              <ul className="list-disc list-inside" data-oid="anki6lq">
                {message.sources.map((source, idx) => (
                  <li key={idx} data-oid="g-n-p3f">
                    {source}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
