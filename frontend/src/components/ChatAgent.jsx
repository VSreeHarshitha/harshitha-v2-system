import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, X, Terminal, Loader2, AlertCircle } from 'lucide-react';

export default function ChatAgent({ isOpen, setIsOpen }) {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hi Harshitha! I am your Portfolio Agent. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    // Initial placeholder
    setMessages(prev => [...prev, { role: 'ai', content: '...' }]);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Admin-Key': 'malla_reddy_2026' 
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) throw new Error(`Server responded with ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedContent = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const cleanedLine = line.replace('data: ', '').trim();
              if (!cleanedLine) continue;
              
              const data = JSON.parse(cleanedLine);
              
              // Only update if content exists
              if (data.content) {
                accumulatedContent += data.content;
                setMessages(prev => {
                  const newMsgs = [...prev];
                  newMsgs[newMsgs.length - 1].content = accumulatedContent;
                  return newMsgs;
                });
              }
            } catch (e) {
              console.error("JSON Parse Error", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Stream Error:", error);
      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1].content = `⚠️ Connection Error: Is the backend running?`;
        return newMsgs;
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="fixed bottom-28 right-10 w-96 h-[500px] glass-card z-50 rounded-3xl flex flex-col overflow-hidden border border-white/10 shadow-2xl backdrop-blur-2xl bg-black/60"
        >
          {/* Header */}
          <div className="p-4 border-b border-white/10 flex justify-between items-center bg-white/5">
            <div className="flex items-center gap-2">
              <Terminal size={18} className="text-purple-400" />
              <span className="text-[10px] font-bold tracking-widest uppercase text-neutral-400">Project P Core</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-neutral-500 hover:text-white transition-colors">
              <X size={18}/>
            </button>
          </div>

          {/* Messages Area */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] p-3 rounded-2xl text-sm ${
                  m.role === 'user' 
                    ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/20' 
                    : 'bg-white/5 text-neutral-200 border border-white/10'
                }`}>
                  {m.content}
                </div>
              </div>
            ))}
          </div>

          {/* Input Area */}
          <div className="p-4 bg-black/40 flex gap-2 border-t border-white/5">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder={isLoading ? "Thinking..." : "Ask Project P..."} 
              disabled={isLoading}
              className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-purple-500 transition-all text-white placeholder:text-neutral-600"
            />
            <button 
              onClick={sendMessage} 
              disabled={isLoading}
              className="p-2 bg-purple-600 rounded-xl hover:bg-purple-500 transition-all flex items-center justify-center min-w-[40px]"
            >
              {isLoading ? <Loader2 className="animate-spin text-white" size={18} /> : <Send size={18} className="text-white" />}
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}