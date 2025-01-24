import { ChatContainer } from "@/components/ChatContainer";

const Index = () => {
  return (
    <div className="min-h-screen w-full bg-[#343541]">
      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-semibold text-white mb-2">PDF Chat Assistant</h1>
          <p className="text-gray-400">
            Ask questions about your PDF documents
          </p>
        </div>
        <ChatContainer />
      </div>
    </div>
  );
};

export default Index;