"use client";

import { useState } from "react";

export function ChatBubble({
  text,
  className,
}: {
  text: string;
  className?: string;
}) {
  return (
    <div className={`p-2 bg-blue-500 rounded-xl ${className}`}>{text}</div>
  );
}

export function ChatUI() {
  const [chats, setChats] = useState<string[]>([]);

  const [currentChat, setCurrentChat] = useState<string>("");

  return (
    <div
      className={`flex grow flex-col justify-between space-y-2 border-2 border-red h-screen`}
    >
      <div className="flex grow flex-col overflow-scroll space-y-2 flex-end">
        {chats.map((chat, idx) => (
          <ChatBubble key={idx} text={chat} className="self-end" />
        ))}
      </div>

      <div className="flex flex-row space-x-4 max-h-[100px]">
        <input
          name="test"
          className="text-black grow rounded-full p-3"
          onChange={(a) => setCurrentChat(a.target.value)}
        />
        <button
          className="rounded-lg bg-blue-400 p-4"
          onClick={() => setChats([...chats, currentChat])}
        >
          Send
        </button>
      </div>
    </div>
  );
}
