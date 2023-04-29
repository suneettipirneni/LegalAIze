"use client";

import { useState } from "react";

export function Chat() {
  const [chats, setChats] = useState<string[]>(["1", "2", "3", "4", "5"]);

  return (
    <div className="flex flex-col items-center justify-between p-24">
      {chats.map((chat, idx) => (
        <div
          key={idx}
          className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex"
        >
          {chat}
        </div>
      ))}
    </div>
  );
}
