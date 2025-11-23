import React, { useState, useRef, useEffect } from 'react';
import { Send, BookOpen, FlaskConical, Sparkles, User, Bot } from 'lucide-react';

function App() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: "Hello! I'm your Treg Research Assistant. I can help you design experiments, find protocols, or research Treg biology. What are you working on today?",
            sources: []
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: userMessage.content }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();

            const botMessage = {
                role: 'assistant',
                content: data.answer,
                sources: data.sources || []
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "I'm sorry, I encountered an error connecting to the server. Please ensure the backend is running.",
                sources: []
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-bio-dark text-slate-100 overflow-hidden">
            {/* Sidebar */}
            <div className="w-64 bg-bio-panel border-r border-slate-700 hidden md:flex flex-col p-4">
                <div className="flex items-center gap-2 mb-8 text-bio-accent">
                    <FlaskConical className="w-8 h-8" />
                    <h1 className="text-xl font-bold tracking-tight">Treg Assistant</h1>
                </div>

                <div className="space-y-4">
                    <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Capabilities</div>
                    <div className="flex items-center gap-3 p-2 rounded hover:bg-slate-700/50 cursor-pointer transition-colors text-sm">
                        <BookOpen className="w-4 h-4 text-bio-secondary" />
                        <span>Literature Search</span>
                    </div>
                    <div className="flex items-center gap-3 p-2 rounded hover:bg-slate-700/50 cursor-pointer transition-colors text-sm">
                        <Sparkles className="w-4 h-4 text-bio-secondary" />
                        <span>Protocol Design</span>
                    </div>
                </div>

                <div className="mt-auto pt-4 border-t border-slate-700">
                    <div className="text-xs text-slate-500">
                        Powered by RAG & LlamaIndex
                    </div>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full">
                {/* Header (Mobile only) */}
                <div className="md:hidden p-4 border-b border-slate-700 flex items-center gap-2 bg-bio-panel">
                    <FlaskConical className="w-6 h-6 text-bio-accent" />
                    <h1 className="font-bold">Treg Assistant</h1>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>

                            {msg.role === 'assistant' && (
                                <div className="w-8 h-8 rounded-full bg-bio-secondary/20 flex items-center justify-center flex-shrink-0 border border-bio-secondary/30">
                                    <Bot className="w-5 h-5 text-bio-secondary" />
                                </div>
                            )}

                            <div className={`max-w-[80%] space-y-2 ${msg.role === 'user' ? 'items-end flex flex-col' : ''}`}>
                                <div className={`p-4 rounded-2xl shadow-sm ${msg.role === 'user'
                                        ? 'bg-bio-accent/10 text-bio-accent border border-bio-accent/20 rounded-tr-none'
                                        : 'bg-bio-panel border border-slate-700 rounded-tl-none'
                                    }`}>
                                    <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                                </div>

                                {/* Sources */}
                                {msg.sources && msg.sources.length > 0 && (
                                    <div className="bg-slate-900/50 rounded-lg p-3 text-xs border border-slate-800 ml-2 animate-in fade-in slide-in-from-top-2">
                                        <div className="font-semibold text-slate-400 mb-2 flex items-center gap-2">
                                            <BookOpen className="w-3 h-3" /> Sources
                                        </div>
                                        <div className="space-y-2">
                                            {msg.sources.map((source, sIdx) => (
                                                <a
                                                    key={sIdx}
                                                    href={source.url}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="block p-2 rounded bg-slate-800/50 hover:bg-slate-700 transition-colors border-l-2 border-bio-secondary truncate"
                                                >
                                                    <div className="font-medium text-slate-300 truncate">{source.title}</div>
                                                    <div className="text-slate-500 mt-0.5">{source.source} • {source.id}</div>
                                                </a>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>

                            {msg.role === 'user' && (
                                <div className="w-8 h-8 rounded-full bg-bio-accent/20 flex items-center justify-center flex-shrink-0 border border-bio-accent/30">
                                    <User className="w-5 h-5 text-bio-accent" />
                                </div>
                            )}
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex gap-4">
                            <div className="w-8 h-8 rounded-full bg-bio-secondary/20 flex items-center justify-center flex-shrink-0 border border-bio-secondary/30">
                                <Bot className="w-5 h-5 text-bio-secondary" />
                            </div>
                            <div className="bg-bio-panel border border-slate-700 p-4 rounded-2xl rounded-tl-none flex items-center gap-2">
                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-bio-dark border-t border-slate-800">
                    <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask about Treg protocols, markers, or clinical trials..."
                            className="w-full bg-bio-panel text-slate-100 placeholder-slate-500 rounded-xl pl-4 pr-12 py-3 border border-slate-700 focus:outline-none focus:border-bio-accent focus:ring-1 focus:ring-bio-accent transition-all shadow-lg"
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={!input.trim() || isLoading}
                            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-bio-accent text-bio-dark rounded-lg hover:bg-sky-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send className="w-4 h-4" />
                        </button>
                    </form>
                    <div className="text-center mt-2">
                        <p className="text-[10px] text-slate-600">
                            AI can make mistakes. Verify important information.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
