"use client";

import { RefObject, useContext, useEffect, useRef, useState } from "react";

import { BsFillCursorFill } from "react-icons/bs";
import { AnimatePresence, motion } from "framer-motion";
import { MoonLoader } from "react-spinners";
import { FilenameContext } from "./FilenameProvided";

interface Message {
  content: string;
  recieved: boolean;
}

const cachedChats = new Map<string, Message[]>();

export function ChatBubble({
  text,
  recieved = false,
  ref,
}: {
  text: string;
  recieved?: boolean;
  ref?: RefObject<HTMLDivElement> | null;
}) {
  const alignClass = recieved ? "self-start" : "self-end";
  const bgClass = recieved
    ? "bg-slate-100 text-black rounded-t-xl rounded-r-xl"
    : "bg-blue-500 shadow-sm text-white rounded-t-xl rounded-l-xl";
  return (
    <motion.div
      ref={ref}
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
      className={`py-2 px-3 ${bgClass} min-w-[40px] text-lg text-left max-w-[60%] ${alignClass}`}
    >
      {text}
    </motion.div>
  );
}

export function ChatUI({ summary }: { summary: string }) {
  const [chats, setChats] = useState<Message[]>([]);
  const [currentChat, setCurrentChat] = useState<string>("");
  const [thinking, setThinking] = useState<boolean>(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [isGeneral, setIsGeneral] = useState<boolean>(false);

  const filename = useContext(FilenameContext);

  useEffect(() => {
    if (filename && cachedChats.has(filename)) {
      setChats(cachedChats.get(filename)!);
    } else {
      setChats([]);
    }
  }, [filename]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }

    cachedChats.set(filename!, chats);
  }, [chats, filename]);

  const submitChat = async () => {
    setThinking(true);
    setCurrentChat("");
    const cachedChats = [...chats, { content: currentChat, recieved: false }];
    setChats(() => cachedChats);
    console.log(chats);
    const res = await fetch(
      "http://localhost:8000/ask?" +
        new URLSearchParams({
          prompt: currentChat,
          filename: filename!,
          general: `${isGeneral}`,
        })
    );

    const data = (await res.json()) as { content: string };

    console.log(data);

    setChats([...cachedChats, { content: data.content, recieved: true }]);
    setThinking(false);
  };

  if (!filename) {
    return (
      <div
        className={`flex grow flex-col justify-center items-center h-full max-w-[1200px] text-black`}
      >
        No file selected
      </div>
    );
  }

  return (
    <div
      className={`flex grow flex-col justify-between h-screen max-w-[1200px]`}
    >
      <div className="flex flex-col space-y-4 p-2 text-black w-full items-center justify-between font-bold border-b border-slate-200">
        <div className="flex flex-row justify-between w-full items-center">
          <span>{filename}</span>
          <button
            className={`rounded-lg border border-black px-3 py-2 ${
              isGeneral ? "bg-black text-white" : ""
            }`}
            onClick={() => setIsGeneral((prev) => !prev)}
          >
            General Mode
          </button>
        </div>
        <span className="font-normal text-slate-500">{summary}</span>
      </div>
      <div className="grow"></div>

      <div
        ref={scrollRef}
        className="flex flex-col overflow-y-auto overflow-x-clip space-y-2 self-end pb-2 px-2 w-full"
      >
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
