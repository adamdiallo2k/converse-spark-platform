import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "@/hooks/use-toast";

export const ApiKeySettings = () => {
  const [llamaParseKey, setLlamaParseKey] = useState('');
  const [openAIKey, setOpenAIKey] = useState('');

  const handleSave = () => {
    if (llamaParseKey) {
      localStorage.setItem('LLAMA_PARSE_API_KEY', llamaParseKey);
    }
    if (openAIKey) {
      localStorage.setItem('OPENAI_API_KEY', openAIKey);
    }
    toast({
      title: "Success",
      description: "API keys saved successfully",
    });
  };

  return (
    <div className="space-y-4 p-4 border rounded-lg">
      <h2 className="text-lg font-semibold">API Settings</h2>
      <div className="space-y-2">
        <Input
          type="password"
          placeholder="LlamaParse API Key"
          value={llamaParseKey}
          onChange={(e) => setLlamaParseKey(e.target.value)}
        />
        <Input
          type="password"
          placeholder="OpenAI API Key"
          value={openAIKey}
          onChange={(e) => setOpenAIKey(e.target.value)}
        />
        <Button onClick={handleSave}>Save API Keys</Button>
      </div>
    </div>
  );
};