import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Input } from '@/components/ui/input';
import { MessageCircle, Send, Bot, User } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export function ChatbotButton() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hi! I'm your university application advisor. I can help you with questions about Ontario university applications, deadlines, essays, and more. How can I help you today?",
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    // Simulate bot response
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Thanks for your question! I'm a demo chatbot. In the full version, I'll be able to help you with application advice, essay reviews, deadline reminders, and more.",
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button 
          size="lg"
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg border-2 border-border z-50"
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-96 border-l-2 border-border flex flex-col p-0">
        <SheetHeader className="border-b-2 border-border p-4">
          <SheetTitle className="flex items-center gap-2 font-bold uppercase tracking-wider">
            <Bot className="h-5 w-5" />
            Application Advisor
          </SheetTitle>
        </SheetHeader>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                'flex gap-3',
                message.role === 'user' ? 'flex-row-reverse' : ''
              )}
            >
              <div className={cn(
                'h-8 w-8 flex items-center justify-center border-2 border-border flex-shrink-0',
                message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'
              )}>
                {message.role === 'user' ? (
                  <User className="h-4 w-4" />
                ) : (
                  <Bot className="h-4 w-4" />
                )}
              </div>
              <div className={cn(
                'flex-1 p-3 border-2 border-border text-sm',
                message.role === 'user' ? 'bg-primary/10' : 'bg-muted'
              )}>
                {message.content}
              </div>
            </div>
          ))}
        </div>

        <div className="border-t-2 border-border p-4">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about applications..."
              className="border-2 border-border"
            />
            <Button 
              onClick={handleSend}
              size="icon"
              className="border-2 border-border flex-shrink-0"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
