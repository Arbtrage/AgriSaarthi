"use client";

import { useState, useRef, useEffect } from "react";
import { ChatInterface, HomeScreen } from "./components";

export default function Home() {
  const [currentView, setCurrentView] = useState<"home" | "chat">("home");
  const [selectedCategory, setSelectedCategory] = useState("crop_info");

  const handleStartChat = (category?: string) => {
    if (category) {
      setSelectedCategory(category);
    }
    setCurrentView("chat");
  };

  const handleBackToHome = () => {
    setCurrentView("home");
  };

  if (currentView === "chat") {
    return (
      <ChatInterface
        selectedCategory={selectedCategory}
        onBackToHome={handleBackToHome}
      />
    );
  }

  return (
    <HomeScreen
      onStartChat={handleStartChat}
      selectedCategory={selectedCategory}
    />
  );
}
