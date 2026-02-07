import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import DTraderHeader from "@/components/layout/DTraderHeader";
import Sidebar from "@/components/layout/Sidebar";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Deriv Defensor",
    description: "AI-Powered Churn Prediction Dashboard",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={cn(inter.className, "bg-gray-50 min-h-screen")}>
                <DTraderHeader />

                <div className="flex">
                    <Sidebar />

                    <main className="flex-1 pt-[48px] md:pl-[240px] min-h-screen">
                        <div className="container mx-auto p-6 max-w-7xl">
                            {children}
                        </div>
                    </main>
                </div>
            </body>
        </html>
    );
}
