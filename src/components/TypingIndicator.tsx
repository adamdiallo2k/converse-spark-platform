export const TypingIndicator = () => {
  return (
    <div className="flex items-center gap-1 px-4 py-2 max-w-[80px] bg-chat-bot rounded-2xl border">
      <div className="w-2 h-2 rounded-full bg-primary/40 animate-typing-dot" />
      <div className="w-2 h-2 rounded-full bg-primary/40 animate-typing-dot [animation-delay:0.2s]" />
      <div className="w-2 h-2 rounded-full bg-primary/40 animate-typing-dot [animation-delay:0.4s]" />
    </div>
  );
};