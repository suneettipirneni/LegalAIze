"use client";

import Image from "next/image";
import { Inter } from "next/font/google";
import { ChatUI } from "@/components/Chat";

import { QueryClient, QueryClientProvider, useQuery } from "react-query";
import { Sidebar } from "@/components/Sidebar";
import { FilenameContext } from "@/components/FilenameProvided";
import { useState } from "react";

const queryClient = new QueryClient();

const inter = Inter({ subsets: ["latin"] });

const sideItems = [
  "Foobar.docx",
  "Baz.docx",
  "Qux.docx",
  "Quux.docx",
  "Quuz.docx",
  "Corge.docx",
  "Grault.docx",
];

export default function Home() {
  const [filename, setFilename] = useState<string | null>(null);
  return (
    <FilenameContext.Provider value={filename}>
      <QueryClientProvider client={queryClient}>
        <main className="flex flex-row justify-center max-h-screen bg-white">
          <div className="flex text-black border-r border-slate-200 max-w-[400px] min-w-[100px] items-center flex-col p-5 space-y-5">
            <h1 className="font-bold text-3xl w-full">Documents</h1>
            <Sidebar onSelect={(item) => setFilename(item.name)} />
          </div>
          <div className="z-10 grow items-center justify-center flex w-full min-h-screen">
            <ChatUI />
          </div>
        </main>
      </QueryClientProvider>
    </FilenameContext.Provider>
  );
}
