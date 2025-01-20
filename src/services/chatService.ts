export const sendMessage = async (message: string): Promise<string> => {
  try {
    // Get API keys from localStorage
    const llamaParseKey = localStorage.getItem('llx-vbWvgnlEl3mre2RbUnAm9FUgmU0Jb1Cs7j6chsSd6sST1qHW');
    const openAIKey = localStorage.getItem('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');

    if (!llamaParseKey || !openAIKey) {
      throw new Error('API keys not found');
    }

    const response = await fetch('http://localhost:5000/api/chat', {
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
      description: error instanceof Error ? error.message : "Failed to send message",
      variant: "destructive",
    });
    throw error;
  }
};