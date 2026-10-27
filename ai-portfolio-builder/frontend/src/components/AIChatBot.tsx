import React, { useState } from 'react';
import { portfolioApi } from '../api/client';

interface AIChatBotProps {
    slug: string;
}

export const AIChatBot: React.FC<AIChatBotProps> = ({ slug }) => {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<{ role: 'user' | 'ai', text: string }[]>([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;
        
        const userMsg = { role: 'user' as const, text: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            // Using the public chat endpoint
            const res = await portfolioApi.getPublicProjects(slug); // Adjusted for the endpoint we built
            // NOTE: In a real app, we'd use a dedicated post request for chat.
            // For this implementation, we call the AI service:
            const aiRes = await fetch(`http://localhost:8000/api/v1/chat?slug=${slug}&query=${encodeURIComponent(input)}`, {
                method: 'POST'
            });
            const data = await aiRes.json();
            setMessages(prev => [...prev, { role: 'ai', text: typeof data === 'string' ? data : data.response }]);
        } catch (e) {
            setMessages(prev => [...prev, { role: 'ai', text: "Sorry, I'm having trouble connecting to my brain right now." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed bottom-6 right-6 w-80 bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col h-96">
            <div className="bg-blue-600 p-4 text-white font-bold flex justify-between items-center">
                <span>Portfolio AI</span>
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <p className="text-gray-400 text-sm text-center italic">Ask me anything about this portfolio!</p>
                )}
                {messages.map((m, i) => (
                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-3 rounded-lg text-sm ${m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'}`}>
                            {m.text}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-gray-400 text-xs italic animate-bounce">AI is thinking...</div>}
            </div>

            <div className="p-3 border-t flex gap-2">
                <input 
                    className="flex-1 text-sm p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Type a question..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                />
                <button 
                    onClick={sendMessage} 
                    disabled={loading}
                    className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
                >
                    Send
                </button>
            </div>
        </div>
    );
};
