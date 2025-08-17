"use client";

import { useState, useRef, useEffect } from "react";

interface ChatMessage {
    id: string;
    question: string;
    response: string;
    category: string;
    timestamp: Date;
}

interface ChatInterfaceProps {
    selectedCategory: string;
    onBackToHome: () => void;
}

export default function ChatInterface({ selectedCategory, onBackToHome }: ChatInterfaceProps) {
    const [question, setQuestion] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
    const [currentStreamingResponse, setCurrentStreamingResponse] = useState("");
    const [currentStreamingMessageId, setCurrentStreamingMessageId] = useState<string | null>(null);

    const chatEndRef = useRef<HTMLDivElement>(null);
    const questionInputRef = useRef<HTMLInputElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatHistory, currentStreamingResponse]);

    // Debug streaming state changes
    useEffect(() => {
        console.log("currentStreamingResponse changed:", currentStreamingResponse);
        console.log("currentStreamingMessageId changed:", currentStreamingMessageId);
    }, [currentStreamingResponse, currentStreamingMessageId]);

    const getCategoryIcon = (category: string) => {
        const icons: { [key: string]: string } = {
            crop_info: "🌾",
            fertilizers: "🌱",
            market_prices: "📊",
            gov_schemes: "🏛️",
            other: "🔍",
        };
        return icons[category] || "🌾";
    };

    const getCategoryName = (category: string) => {
        return category.replace(/_/g, " ");
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!question.trim() || isLoading) return;

        const newMessage: ChatMessage = {
            id: Date.now().toString(),
            question: question.trim(),
            response: "",
            category: selectedCategory,
            timestamp: new Date(),
        };

        setChatHistory(prev => [...prev, newMessage]);
        setQuestion("");
        setIsLoading(true);
        setCurrentStreamingMessageId(newMessage.id);
        setCurrentStreamingResponse("");

        await handleStreamingChat(newMessage);
    };

    const handleStreamingChat = async (message: ChatMessage) => {
        try {
            console.log("Starting streaming chat for message:", message.id);
            const response = await fetch(process.env.NEXT_PUBLIC_API_URL!, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    category: message.category,
                    question: message.question,
                    language: "en-US",
                }),
            });

            console.log("Response received:", response.status, response.ok);
            console.log("Response headers:", Object.fromEntries(response.headers.entries()));

            if (response.ok && response.body) {
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let accumulatedResponse = "";

                console.log("Starting to read stream...");
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        console.log("Stream finished");
                        break;
                    }

                    const chunk = decoder.decode(value, { stream: true });
                    if (chunk) {
                        accumulatedResponse += chunk;
                        // Update the streaming response in real-time
                        setCurrentStreamingResponse(accumulatedResponse);
                        console.log("Streaming chunk:", chunk);
                        console.log("Accumulated response:", accumulatedResponse);
                    }
                }

                console.log("Final accumulated response:", accumulatedResponse);
                // Update the message with the complete response
                updateMessageResponse(message.id, accumulatedResponse);
                setCurrentStreamingResponse("");
                setCurrentStreamingMessageId(null);
            } else {
                const errorText = await response.text();
                console.log("Error response:", errorText);
                updateMessageResponse(message.id, `Error: ${response.status} - ${errorText}`);
            }
        } catch (error) {
            console.error("Streaming error:", error);
            updateMessageResponse(message.id, "An error occurred while processing your request.");
        } finally {
            setIsLoading(false);
            setCurrentStreamingMessageId(null);
        }
    };

    const updateMessageResponse = (messageId: string, response: string) => {
        setChatHistory(prev =>
            prev.map(msg =>
                msg.id === messageId ? { ...msg, response } : msg
            )
        );
    };

    return (
        <div className="h-screen flex flex-col bg-white">
            {/* Header */}
            <header className="flex-shrink-0 bg-white border-b border-gray-200 px-4 py-3">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <button
                            onClick={onBackToHome}
                            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg"
                        >
                            ←
                        </button>
                        <div className="w-8 h-8 rounded-lg flex items-center justify-center">
                            <span className="text-white text-sm font-bold">{getCategoryIcon(selectedCategory)}</span>
                        </div>
                        <div>
                            <h1 className="font-semibold text-gray-900 capitalize">
                                {getCategoryName(selectedCategory)}
                            </h1>
                            <p className="text-sm text-gray-500">AI Agricultural Assistant</p>
                        </div>
                    </div>
                </div>
            </header>

            {/* Chat Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {chatHistory.length === 0 ? (
                    <div className="text-center py-12">
                        <div className="text-6xl mb-4">{getCategoryIcon(selectedCategory)}</div>
                        <h3 className="text-lg font-medium text-gray-900 mb-2">
                            Welcome to {getCategoryName(selectedCategory)}!
                        </h3>
                        <p className="text-gray-500">
                            Ask me anything about {getCategoryName(selectedCategory).toLowerCase()} and farming.
                        </p>
                    </div>
                ) : (
                    chatHistory.map((message) => (
                        <div key={message.id} className="space-y-3">
                            {/* User Question */}
                            <div className="flex justify-end">
                                <div className="max-w-[80%] bg-green-600 text-white p-3 rounded-lg rounded-br-none">
                                    <p className="text-sm">{message.question}</p>
                                    <div className="flex items-center justify-between mt-2 text-xs opacity-75">
                                        <span className="capitalize">{getCategoryName(message.category)}</span>
                                        <span>{message.timestamp.toLocaleTimeString()}</span>
                                    </div>
                                </div>
                            </div>

                            {/* AI Response */}
                            <div className="flex justify-start">
                                <div className="max-w-[80%] bg-white text-gray-900 p-3 rounded-lg rounded-bl-none border border-gray-200">
                                    {message.response ? (
                                        <div>
                                            <p className="text-sm whitespace-pre-wrap">{message.response}</p>
                                            <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                                                <span className="capitalize">{getCategoryName(message.category)}</span>
                                                <span>{message.timestamp.toLocaleTimeString()}</span>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="flex items-center space-x-2">
                                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600"></div>
                                            <span className="text-sm text-gray-500">Thinking...</span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))
                )}

                {/* Current Streaming Response */}
                {currentStreamingResponse && currentStreamingMessageId && (
                    <div className="flex justify-start">
                        <div className="max-w-[80%] bg-white text-gray-900 p-3 rounded-lg rounded-bl-none border border-gray-200">
                            <p className="text-sm whitespace-pre-wrap">
                                {currentStreamingResponse}
                                <span className="inline-block w-2 h-4 bg-green-600 ml-1 animate-pulse"></span>
                            </p>
                            <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                                <span className="capitalize">{getCategoryName(selectedCategory)}</span>
                                <span className="text-green-600">Streaming...</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={chatEndRef} />
            </div>

            {/* Chat Input - Fixed at Bottom */}
            <div className="flex-shrink-0 bg-white border-t border-gray-200 p-4">
                <form onSubmit={handleSubmit} className="flex space-x-3">
                    <input
                        ref={questionInputRef}
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder={`Ask about ${getCategoryName(selectedCategory)}...`}
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!question.trim() || isLoading}
                        className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {isLoading ? (
                            <div className="flex items-center space-x-2">
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                <span>Ask</span>
                            </div>
                        ) : (
                            "Ask"
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
}
