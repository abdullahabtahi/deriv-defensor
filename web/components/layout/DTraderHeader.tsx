"use client"

import Link from "next/link"
import { Bell, Search, Settings, User } from "lucide-react"

export default function DTraderHeader() {
    return (
        <header className="fixed top-0 left-0 right-0 z-50 h-[48px] bg-white border-b border-gray-200 shadow-sm flex items-center justify-between px-4">
            {/* Left: Branding & Navigation */}
            <div className="flex items-center gap-6">
                {/* Deriv Logo (Simulated) */}
                <Link href="/" className="flex items-center gap-2">
                    <svg width="24" height="24" viewBox="0 0 1024 1024" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M512 0C229.23 0 0 229.23 0 512s229.23 512 512 512 512-229.23 512-512S794.77 0 512 0zm0 945.45c-239.1 0-433.45-194.35-433.45-433.45S272.9 78.55 512 78.55 945.45 272.9 945.45 512 751.1 945.45 512 945.45z" fill="#FF444F" />
                        <path d="M669.6 424.8c0-101.6-82.4-184-184-184s-184 82.4-184 184v174.4h73.6V424.8c0-60.8 49.6-110.4 110.4-110.4s110.4 49.6 110.4 110.4v174.4h73.6V424.8z" fill="#FF444F" />
                    </svg>
                    <span className="font-bold text-lg text-gray-900 tracking-tight">Deriv Defensor</span>
                </Link>

                {/* Primary Nav */}
                <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
                    <Link href="/dashboard" className="text-gray-900 font-bold border-b-2 border-deriv-red py-[13px]">
                        Dashboard
                    </Link>
                    <Link href="/reports" className="hover:text-deriv-red transition-colors">
                        Intervention Log
                    </Link>
                    {/* Partner Analysis accessed via Dashboard partner rows */}
                </nav>
            </div>

            {/* Right: Account & Notifications */}
            <div className="flex items-center gap-4">
                {/* Account Switcher - Removed for demo */}
                {/* 
                <div className="flex flex-col items-end cursor-pointer group">
                    <span className="text-xs text-gray-500 uppercase font-semibold">Real Account</span>
                    <div className="flex items-center gap-1">
                        <span className="text-green-600 text-sm font-bold">10,000.00 USD</span>
                        <svg width="10" height="6" viewBox="0 0 10 6" fill="none" className="group-hover:rotate-180 transition-transform">
                            <path d="M1 1L5 5L9 1" stroke="#333333" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </div>
                </div>

                <div className="h-6 w-[1px] bg-gray-200 mx-1"></div>
                */}

                {/* Icons */}
                <button className="text-gray-600 hover:text-gray-900 transition-colors p-1">
                    <Bell size={18} />
                </button>
                <button className="text-gray-600 hover:text-gray-900 transition-colors p-1">
                    <User size={18} />
                </button>
            </div>
        </header>
    )
}
