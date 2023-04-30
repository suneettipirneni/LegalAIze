"use client";

import Image from "next/image";
import { Inter } from "next/font/google";
import { ChatUI } from "@/components/Chat";

import { QueryClient, QueryClientProvider, useQuery } from "react-query";
import { Sidebar } from "@/components/Sidebar";
import { FilenameContext } from "@/components/FilenameProvided";
import { useState, FormEvent, ChangeEvent } from "react";
import { RxFilePlus } from "react-icons/rx";
import { BeatLoader, MoonLoader } from "react-spinners";

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
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [summary, setSummary] = useState<string>("");

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    console.log("called");
    const file = event.target.files && event.target.files[0];
    console.log(file);
    setSelectedFile(file ?? null);

    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("document", file);

    console.log(formData);

    setIsUploading(true);

    console.log("Uploading file...");

    await fetch("http://localhost:8000/fileupload", {
      method: "POST",
      body: formData,
    });

    setIsUploading(false);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log("called");

    if (!selectedFile) {
      return;
    }

    const formData = new FormData();
    formData.append("document", selectedFile);

    console.log(formData);

    setIsUploading(true);

    console.log("Uploading file...");

    await fetch("http://localhost:8000/fileupload", {
      method: "POST",
      body: formData,
    });

    setIsUploading(false);
  };

  return (
    <FilenameContext.Provider value={filename}>
      <QueryClientProvider client={queryClient}>
        <main className="flex flex-row justify-center max-h-screen bg-white">
          <div className="flex text-black border-r border-slate-200 max-w-[400px] min-w-[100px] items-center flex-col p-5 space-y-5">
            <div className="flex flex-row justify-space-between w-full">
              <h1 className="font-bold self-start text-3xl w-full">
                Documents
              </h1>
              <form
                onSubmit={handleSubmit}
                className="flex flex-row items-center"
              >
                <label htmlFor="file-upload" />
                <input
                  type="file"
                  id="file-upload"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                />
                <button
                  type="button"
                  onClick={() => {
                    console.log("test");
                    document?.getElementById("file-upload")?.click();
                  }}
                >
                  {isUploading ? (
                    <BeatLoader size={32} />
                  ) : (
                    <RxFilePlus size={32} />
                  )}
                </button>
                {/* <button type="submit">Upload</button> */}
              </form>
              {/* <button className="bg-slate-100 rounded-full p-2">
                <RxFilePlus />
              </button> */}
            </div>
            <Sidebar
              onSelect={(item) => {
                setFilename(item.name);
                setSummary(item.summary);
              }}
            />
          </div>
          <div className="z-10 grow items-center justify-center flex w-full min-h-screen">
            <ChatUI summary={summary} />
          </div>
        </main>
      </QueryClientProvider>
    </FilenameContext.Provider>
  );
}
