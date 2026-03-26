import React from 'react';
import { motion } from 'framer-motion';
import { Music, Brain, Code, Sparkles, Mic2, Cpu } from 'lucide-react';

// This is a reusable "Animated Card" component
const Card = ({ children, className, delay = 0 }) => (
  <motion.div 
    initial={{ opacity: 0, y: 30 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8, delay, ease: [0.16, 1, 0.3, 1] }}
    className={`glass-card glass-hover rounded-bento p-8 ${className}`}
  >
    {children}
  </motion.div>
);

export default function App() {
  return (
    <div className="min-h-screen p-6 md:p-16 max-w-7xl mx-auto space-y-6">
      {/* 12-Column Grid System */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 auto-rows-[160px]">
        
        {/* Main Header / Bio */}
        <Card className="md:col-span-8 md:row-span-3 flex flex-col justify-end relative overflow-hidden">
          <div className="absolute top-8 right-8 text-purple-500/20"><Sparkles size={120} /></div>
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter mb-4 bg-gradient-to-r from-white to-neutral-500 bg-clip-text text-transparent">
            HARSHITHA
          </h1>
          <p className="text-xl text-neutral-400 max-w-lg leading-relaxed">
            3rd Year B.Tech AI/ML Specialist. Building the bridge between 
            <span className="text-purple-400"> neural networks </span> and 
            <span className="text-purple-400"> musical notes</span>.
          </p>
        </Card>

        {/* Live Academic Stat */}
        <Card className="md:col-span-4 md:row-span-2 flex flex-col justify-center items-center text-center bg-purple-600/5" delay={0.2}>
          <Cpu className="text-purple-500 mb-4" />
          <span className="text-xs font-bold tracking-[0.2em] text-neutral-500 uppercase">Current CGPA</span>
          <h2 className="text-7xl font-black mt-2">9.5</h2>
          <div className="mt-4 flex items-center gap-2 text-[10px] text-green-400 bg-green-400/10 px-3 py-1 rounded-full">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" /> Verified Live
          </div>
        </Card>

        {/* Music / Band Card */}
        <Card className="md:col-span-4 md:row-span-3 flex flex-col justify-between border-l-4 border-purple-500" delay={0.4}>
          <div className="flex justify-between items-center">
            <Mic2 className="text-purple-400" />
            <Music className="text-neutral-700" size={16} />
          </div>
          <div>
            <h3 className="text-3xl font-bold italic tracking-tighter">DAKSHIN LOKA</h3>
            <p className="text-neutral-500 text-sm mt-2">Lead Vocalist. Merging Carnatic soul with AI-driven soundscapes.</p>
          </div>
        </Card>

        {/* Tech Stack / Innovations */}
        <Card className="md:col-span-4 md:row-span-2" delay={0.3}>
          <div className="flex gap-2 mb-6">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <div className="w-2 h-2 rounded-full bg-yellow-500" />
            <div className="w-2 h-2 rounded-full bg-green-500" />
          </div>
          <h4 className="text-lg font-bold mb-4">Core Innovations</h4>
          <ul className="space-y-3 text-sm text-neutral-400">
            <li className="flex items-center gap-2 hover:text-white transition-colors cursor-default">
              <div className="w-1 h-1 bg-purple-500" /> Swaraalaya AI Teacher
            </li>
            <li className="flex items-center gap-2 hover:text-white transition-colors cursor-default">
              <div className="w-1 h-1 bg-purple-500" /> Smart Helmet Logic
            </li>
          </ul>
        </Card>

      </div>

      {/* The floating AI Agent Toggle */}
      <motion.button 
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="fixed bottom-10 right-10 w-16 h-16 bg-white text-black rounded-full flex items-center justify-center shadow-2xl z-50"
      >
        <Brain size={28} />
      </motion.button>
    </div>
  );
}