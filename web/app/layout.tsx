import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AgriSaarthi - AI-Powered Agricultural Assistant",
  description: "Get expert advice on farming, crops, fertilizers, market prices, and government schemes with our AI agricultural assistant.",
  keywords: "agriculture, farming, AI assistant, crop advice, fertilizers, market prices, government schemes",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
