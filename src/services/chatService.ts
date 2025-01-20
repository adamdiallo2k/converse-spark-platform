import { toast } from "@/hooks/use-toast";

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export const sendMessage = async (message: string): Promise<string> => {
  try {
    // Get API keys from localStorage (temporary solution)
    const llamaParseKey = localStorage.getItem('LLAMA_PARSE_API_KEY');
    const openAIKey = localStorage.getItem('OPENAI_API_KEY');

    if (!llamaParseKey || !openAIKey) {
      throw new Error('API keys not found. Please set them in the settings.');
    }

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Llama-Parse-Key': llamaParseKey,
        'X-OpenAI-Key': openAIKey,
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    toast({
      title: "Error",
      description: error instanceof Error ? error.message : "Failed to send message. Please try again.",
      variant: "destructive",
    });
    throw error;
  }
};