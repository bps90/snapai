import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SnapAI",
  description: "A Simulator for Network Algorithms and Protocols in Python",
};

interface IRootLayoutProps {
  readonly children: React.ReactNode;
}

export default function RootLayout({ children }: IRootLayoutProps) {
  return (
    <html lang="en">
      <body className={`${geistSans.className} ${geistMono.className} antialiased`}>
        {children}
      </body>
    </html>
  );
}
