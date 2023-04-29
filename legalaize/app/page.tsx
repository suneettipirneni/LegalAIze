import Image from "next/image";
import { Inter } from "next/font/google";
import { ChatUI } from "@/components/Chat";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-between max-h-screen">
      <div className="z-10 grow max-w-5xl items-center justify-between flex w-full min-h-screen">
        <ChatUI />
      </div>
    </main>
  );
}
