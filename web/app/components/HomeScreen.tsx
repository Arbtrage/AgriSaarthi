"use client";

import { useState, useEffect } from "react";

interface Category {
    name: string;
    description: string;
}

interface HomeScreenProps {
    onStartChat: (category?: string) => void;
    selectedCategory: string;
}

export default function HomeScreen({ onStartChat, selectedCategory }: HomeScreenProps) {
    const [categories, setCategories] = useState<Category[]>([]);

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/agents/categories`);
            const data = await response.json();

            const mappedCategories = data.primary_categories.map((cat: string) => ({
                name: cat,
                description: data.descriptions[cat] || "Agricultural information and advice"
            }));

            setCategories(mappedCategories);
        } catch (error) {
            console.error("Failed to fetch categories:", error);
        }
    };

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

    const getCategoryColor = (category: string) => {
        const colors: { [key: string]: string } = {
            crop_info: "bg-green-100 text-green-800 border-green-200",
            fertilizers: "bg-blue-100 text-blue-800 border-blue-200",
            market_prices: "bg-purple-100 text-purple-800 border-purple-200",
            gov_schemes: "bg-orange-100 text-orange-800 border-orange-200",
            other: "bg-gray-100 text-gray-800 border-gray-200",
        };
        return colors[category] || "bg-gray-100 text-gray-800 border-gray-200";
    };

    return (
        <div className="min-h-screen bg-white">
            {/* Header */}
            <header className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-full flex items-center justify-center">
                            <span className="text-white text-lg font-bold">🌾</span>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Welcome back!</p>
                            <h1 className="text-lg font-semibold text-gray-900">AgriSaarthi</h1>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-4xl mx-auto px-6 py-12">
                {/* Hero Section */}
                <div className="text-center mb-16">
                    <div className="w-32 h-32 rounded-full mx-auto mb-6 flex items-center justify-center">
                        <span className="text-white text-4xl">🌾</span>
                    </div>
                    <h2 className="text-4xl font-bold text-gray-900 mb-4">
                        Hello, I'm AgriSaarthi
                    </h2>
                    <p className="text-lg text-gray-600 mb-8">
                        Your AI agricultural assistant. Get expert advice on farming, crops, fertilizers, market prices, and government schemes.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button
                            onClick={() => onStartChat()}
                            className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
                        >
                            Open Chat
                        </button>
                        <button
                            onClick={() => window.open("https://elevenlabs.io/app/talk-to?agent_id=agent_2201k29qy875eqwadz4g9vw7n2ck", "_blank")}
                            className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium"
                        >
                            Talk to me
                        </button>
                    </div>
                </div>

                {/* Feature Cards */}
                <div className="space-y-4">
                    {/* Quick Chat Card */}
                    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between">
                            <div className="flex-1">
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                    Ask anything AgriSaarthi
                                </h3>
                                <div className="flex items-center space-x-3">
                                    <input
                                        type="text"
                                        placeholder="Ask anything AgriSaarthi"
                                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                                        onKeyPress={(e) => {
                                            if (e.key === 'Enter' && e.currentTarget.value.trim()) {
                                                onStartChat();
                                            }
                                        }}
                                    />
                                    <button className="p-2 text-gray-500 hover:text-gray-700">
                                        🎤
                                    </button>
                                    <button
                                        onClick={() => onStartChat()}
                                        className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                                    >
                                        ✈️
                                    </button>
                                </div>
                            </div>
                            <button className="ml-4 p-2 text-gray-400 hover:text-gray-600">
                                →
                            </button>
                        </div>
                    </div>

                    {/* Category Cards */}
                    {categories.map((category) => (
                        <div
                            key={category.name}
                            className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                            onClick={() => onStartChat(category.name)}
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-4">
                                    <span className="text-2xl">{getCategoryIcon(category.name)}</span>
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-900 capitalize">
                                            {category.name.replace(/_/g, " ")}
                                        </h3>
                                        <p className="text-gray-600">{category.description}</p>
                                    </div>
                                </div>
                                <button className="p-2 text-gray-400 hover:text-gray-600">
                                    →
                                </button>
                            </div>
                        </div>
                    ))}

                    {/* Additional Feature Cards */}
                    {/* <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                                <span className="text-2xl">📊</span>
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-900">
                                        Get Market Insights
                                    </h3>
                                    <p className="text-gray-600">Real-time prices and market trends for agricultural products.</p>
                                </div>
                            </div>
                            <button className="p-2 text-gray-400 hover:text-gray-600">
                                →
                            </button>
                        </div>
                    </div>

                    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                                <span className="text-2xl">🏛️</span>
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-900">
                                        Government Schemes
                                    </h3>
                                    <p className="text-gray-600">Information about subsidies, loans, and support programs.</p>
                                </div>
                            </div>
                            <button className="p-2 text-gray-400 hover:text-gray-600">
                                →
                            </button>
                        </div>
                    </div> */}
                </div>
            </main>
        </div>
    );
}
