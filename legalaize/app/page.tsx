import Image from "next/image";
import { Inter } from "next/font/google";
import { ChatUI } from "@/components/Chat";

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
  return (
    <main className="flex flex-row justify-center max-h-screen bg-white">
      <div className="flex text-black border-r border-slate-200 max-w-[400px] min-w-[100px] items-center flex-col p-5 space-y-5">
        <h1 className="font-bold text-3xl w-full">Documents</h1>
        <div className="space-y-2 w-full overflow-auto">
          {sideItems.map((item, idx) => (
            <div
              key={idx}
              className="flex flex-col items-start space-y-1 w-full max-h-[200px] bg-slate-100 rounded-xl p-2 hover:bg-slate-50"
            >
              <span className="font-lg font-bold">{item}</span>
              <span className="grow font-mono text-sm text-ellipsis break-words line-clamp-4 max-w-full">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Est
                lorem ipsum dolor sit. Quis blandit turpis cursus in hac.
                Sollicitudin nibh sit amet commodo nulla facilisi nullam.
                Adipiscing commodo elit at imperdiet dui accumsan. Massa vitae
                tortor condimentum lacinia quis vel. Etiam non quam lacus
                suspendisse. Semper viverra nam libero justo laoreet sit amet.
                Egestas fringilla phasellus faucibus scelerisque. Condimentum
                vitae sapien pellentesque habitant morbi tristique senectus et.
                Turpis massa tincidunt dui ut ornare. Tristique nulla aliquet
                enim tortor at.
              </span>
            </div>
          ))}
        </div>
      </div>
      <div className="z-10 grow items-center justify-center flex w-full min-h-screen">
        <ChatUI />
      </div>
    </main>
  );
}
