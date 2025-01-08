import { cn } from "@/lib/utils";
import { format } from "date-fns";

interface ChatMessageProps {
  content: string;
  isUser: boolean;
  timestamp: Date;
}

export const ChatMessage = ({ content, isUser, timestamp }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex w-full animate-fade-in",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "relative max-w-[80%] rounded-2xl px-4 py-2 shadow-sm",
          isUser
            ? "bg-chat-user text-primary"
            : "bg-chat-bot text-primary border"
        )}
      >
        <p className="text-sm">{content}</p>
        <span className="absolute -bottom-5 text-xs text-muted-foreground">
          {format(timestamp, "HH:mm")}
        </span>
      </div>
    </div>
  );
};