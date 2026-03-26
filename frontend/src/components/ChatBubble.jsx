import React, { useState } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';

export default function ChatBubble() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="glass-card w-80 h-96 rounded-2xl flex flex-col shadow-2xl bg-black/40 backdrop-blur-md border border-white/10">
          <div className="p-4 border-b border-white/10 flex justify-between items-center bg-purple-600/20 rounded-t-2xl">
            <span className="font-bold text-sm">Harshitha's AI Agent</span>
            <button onClick={() => setIsOpen(false)}><X size={18} /></button>
          </div>
          <div className="flex-1 p-4 overflow-y-auto text-sm text-neutral-300">
            Hi! Ask me about Harshitha's projects at Malla Reddy University.
          </div>
          <div className="p-4 border-t border-white/10 flex gap-2">
            <input type="text" placeholder="Ask me anything..." className="bg-white/5 border border-white/10 rounded-full px-4 py-2 text-xs w-full outline-none" />
            <button className="bg-purple-600 p-2 rounded-full"><Send size={14} /></button>
          </div>
        </div>
      ) : (
        <button onClick={() => setIsOpen(true)} className="bg-purple-600 p-4 rounded-full shadow-lg">
          <MessageCircle className="text-white" />
        </button>
      )}
    </div>
  );
}