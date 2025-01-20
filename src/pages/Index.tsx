import { ChatContainer } from "@/components/ChatContainer";
import { ApiKeySettings } from "@/components/ApiKeySettings";

const Index = () => {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center p-4 bg-secondary/30">
      <div className="w-full max-w-2xl mb-8 text-center">
        <h1 className="text-4xl font-semibold mb-2">Welcome to Chat</h1>
        <p className="text-muted-foreground">
          Start a conversation with our AI assistant
        </p>
      </div>
      <ApiKeySettings />
      <div className="h-8" /> {/* Spacer */}
      <ChatContainer />
    </div>
  );
};

export default Index;