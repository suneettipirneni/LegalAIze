import { useContext } from "react";
import { useQuery } from "react-query";
import { FilenameContext } from "./FilenameProvided";

export interface SidebarItem {
  name: string;
  summary: string;
}

export interface SidebarProps {
  onSelect(item: SidebarItem): void;
}

export function Sidebar({ onSelect }: SidebarProps) {
  const { isLoading, error, data } = useQuery<SidebarItem[]>("docs", () =>
    fetch("http://localhost:8000/documents").then((res) => res.json())
  );

  const filename = useContext(FilenameContext);

  return (
    <div className="space-y-2 w-full overflow-auto">
      {data &&
        data.map((item, idx) => (
          <div
            key={idx}
            className={`flex flex-col items-start space-y-1 w-full max-h-[200px] rounded-xl p-2  ${
              filename === item.name
                ? "bg-blue-500 text-white"
                : "hover:bg-slate-50"
            }`}
            onClick={() => onSelect(item)}
          >
            <span className="font-lg font-bold">{item.name}</span>
            <span className="grow font-mono text-sm text-ellipsis break-words line-clamp-4 max-w-full">
              {item.summary}
            </span>
          </div>
        ))}
    </div>
  );
}
