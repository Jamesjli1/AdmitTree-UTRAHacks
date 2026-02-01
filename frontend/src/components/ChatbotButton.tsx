import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { MessageCircle, Send, Bot, User, Loader2, X, Minimize2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export function ChatbotButton() {
  const [isOpen, setIsOpen] = useState(false);
  
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hi! I'm your university application advisor. Ask me about admission averages, co-op programs, or prerequisites!",
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading, isOpen]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    const userText = input;
    const userMessage: Message = {
      id: Date.now().toString(),
      content: userText,
      role: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const API_URL = import.meta.env.PROD 
        ? "https://your-digital-ocean-app-name.ondigitalocean.app" 
        : "http://localhost:5001";

      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userText }),
      });

      const data = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.reply || "Sorry, I didn't catch that.",
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting to the server right now.",
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col items-end space-y-4">
      
      {/* THE CHAT WINDOW */}
      {isOpen && (
        <Card className="w-[350px] h-[500px] flex flex-col border-2 border-border animate-in slide-in-from-bottom-5 fade-in duration-300">
          {/* Header */}
          <CardHeader className="p-4 border-b bg-primary text-primary-foreground rounded-t-sm flex flex-row items-center justify-between space-y-0">
            <div className="flex items-center gap-2 font-bold">
              <Bot className="h-5 w-5" />
              <span>AdmitTree AI</span>
            </div>
            <Button 
              variant="ghost" 
              size="icon" 
              className="h-6 w-6 text-primary-foreground hover:bg-primary-foreground/20"
              onClick={() => setIsOpen(false)}
            >
              <Minimize2 className="h-4 w-4" />
            </Button>
          </CardHeader>
          
          {/* Messages */}
          <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  'flex gap-3',
                  message.role === 'user' ? 'flex-row-reverse' : ''
                )}
              >
                <div className={cn(
                  'h-8 w-8 flex items-center justify-center border-2 border-border flex-shrink-0 rounded-md',
                  message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'
                )}>
                  {message.role === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                </div>
                <div className={cn(
                  'flex-1 p-3 border text-sm rounded-lg',
                  message.role === 'user' ? 'bg-primary/10 border-primary/20' : 'bg-muted/50 border-border'
                )}>
                  {message.content}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex gap-3">
                <div className="h-8 w-8 flex items-center justify-center border flex-shrink-0 rounded-md bg-muted">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="p-3 border text-sm rounded-lg bg-muted/50 flex items-center">
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Thinking...
                </div>
              </div>
            )}
            <div ref={scrollRef} />
          </CardContent>

          {/* Input */}
          <CardFooter className="p-3 border-t bg-muted/20">
            <div className="flex w-full gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask a question..."
                className="flex-1"
                disabled={isLoading}
              />
              <Button 
                onClick={handleSend}
                size="icon"
                disabled={isLoading}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardFooter>
        </Card>
      )}

      {/* THE TOGGLE BUTTON (Clean, No Shadow) */}
      <Button 
        onClick={() => setIsOpen(!isOpen)}
        size="lg"
        className={cn(
          "h-14 w-14 rounded-2xl border-2 border-border transition-all", 
          // REMOVED 'shadow-xl'
          isOpen ? "bg-muted text-foreground" : ""
        )}
      >
        {isOpen ? <X className="h-6 w-6" /> : <MessageCircle className="h-6 w-6" />}
      </Button>
    </div>
  );
}