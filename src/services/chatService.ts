import { toast } from "@/hooks/use-toast";

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export const sendMessage = async (message: string): Promise<string> => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
      description: "Failed to send message. Please try again.",
      variant: "destructive",
    });
    throw error;
  }
};