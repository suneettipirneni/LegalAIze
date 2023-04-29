"use client";

import { useState } from "react";

import { BsFillCursorFill } from "react-icons/bs";
import { AnimatePresence, motion } from "framer-motion";
import { MoonLoader } from "react-spinners";

interface Message {
  content: string;
  recieved: boolean;
}

export function ChatBubble({
  text,
  recieved = false,
}: {
  text: string;
  recieved?: boolean;
}) {
  const alignClass = recieved ? "self-start" : "self-end";
  const bgClass = recieved
    ? "bg-slate-100 text-black"
    : "bg-blue-500 shadow-sm text-white";
  return (
    <motion.div
      initial={{ opacity: 0, x: 100, scale: 0.1, rotate: 5 }}
      animate={{ opacity: 1, x: 0, scale: 1, rotate: 0 }}
      transition={{
        duration: 0.5,
        ease: "easeOut",
        type: "spring",
        damping: 5,
        stiffness: 70,
        restDelta: 0.5,
      }}
      className={`py-2 px-3 ${bgClass} rounded-xl min-w-[40px] text-lg text-left max-w-[60%] ${alignClass}`}
    >
      {text}
    </motion.div>
  );
}

const messages: Message[] = [
  {
    content: "Hello",
    recieved: true,
  },
  {
    content: "Hi",
    recieved: false,
  },
  {
    content: "How are you?",
    recieved: true,
  },
  {
    content: "Good",
    recieved: false,
  },
];

export function ChatUI() {
  const [chats, setChats] = useState<Message[]>(messages);
  const [currentChat, setCurrentChat] = useState<string>("");
  const [thinking, setThinking] = useState<boolean>(false);

  const submitChat = async () => {
    setThinking(true);
    const res = await fetch(
      "http://localhost:8000/summarize?filename=test.docx"
    );

    const data = (await res.json()) as { summary: string };

    console.log(data);

    setChats([...chats, { content: data.summary, recieved: true }]);
    setThinking(false);
    setCurrentChat("");
  };

  return (
    <div
      className={`flex grow flex-col justify-between h-screen max-w-[1200px]`}
    >
      <div className="grow"></div>
      <div className="flex flex-col overflow-y-auto overflow-x-clip space-y-2 self-end pb-2 px-2 w-full">
        {chats.map((chat, idx) => (
          <ChatBubble key={idx} text={chat.content} recieved={chat.recieved} />
        ))}
      </div>

      <AnimatePresence>
        <motion.div
          exit={{ opacity: 0, x: 100 }}
          className="flex flex-row space-x-4 max-h-[100px] p-2"
        >
          <motion.input
            layout
            name="test"
            transition={{ duration: 0.5, type: "spring" }}
            className="text-black grow rounded-full px-3 py-2 border border-slate-300"
            onChange={(a) => setCurrentChat(a.target.value)}
            value={currentChat}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                submitChat();
              }
            }}
          />

          {thinking ? (
            <MoonLoader
              color="blue"
              loading={true}
              size={28}
              speedMultiplier={0.7}
            />
          ) : (
            currentChat.length > 0 && (
              <motion.button
                layout
                initial={{ opacity: 0, x: 0, scale: 0 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                transition={{
                  duration: 0.5,
                  type: "spring",
                }}
                exit={{ opacity: 0, scale: 0 }}
                className="rounded-full bg-blue-500 p-4 text-white"
                disabled={currentChat.length === 0}
                onClick={submitChat}
              >
                <BsFillCursorFill />
              </motion.button>
            )
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
