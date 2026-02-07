"use client"

import { useState, useEffect } from "react"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge" // Assuming you have a Badge component or use shadcn
import { Brain, Sparkles, Copy, CheckCircle, Mail, Loader2, AlertTriangle } from "lucide-react"
import { mockGenAIAnalysis, GenAIAnalysis } from "@/services/genai"
import { motion, AnimatePresence } from "framer-motion"

interface PartnerGenAIModalProps {
    isOpen: boolean;
    onClose: () => void;
    partnerId: string;
    riskScore: number;
}

export function PartnerGenAIModal({ isOpen, onClose, partnerId, riskScore }: PartnerGenAIModalProps) {
    const [loading, setLoading] = useState(false);
    const [analysis, setAnalysis] = useState<GenAIAnalysis | null>(null);
    const [copied, setCopied] = useState(false);

    useEffect(() => {
        if (isOpen && partnerId) {
            setLoading(true);
            setAnalysis(null);

            // Fetch analysis
            mockGenAIAnalysis(partnerId)
                .then(data => {
                    setAnalysis(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error(err);
                    setLoading(false);
                });
        }
    }, [isOpen, partnerId]);

    const handleCopyEmail = () => {
        if (analysis) {
            navigator.clipboard.writeText(`Subject: ${analysis.emailSubject}\n\n${analysis.emailBody}`);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    }

    return (
        <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="sm:max-w-[700px] border-deriv-red/20 shadow-2xl bg-white">
                <DialogHeader className="border-b border-gray-100 pb-4">
                    <div className="flex items-center justify-between">
                        <DialogTitle className="flex items-center gap-2 text-xl font-bold text-gray-900">
                            <Brain className="text-deriv-red" />
                            AI Risk Analysis
                        </DialogTitle>
                        <Badge variant="outline" className={`
                            ${riskScore > 80 ? 'bg-red-50 text-red-600 border-red-200' : 'bg-yellow-50 text-yellow-600 border-yellow-200'}
                            font-mono text-xs px-2 py-0.5
                        `}>
                            Risk Score: {riskScore}%
                        </Badge>
                    </div>
                    <DialogDescription className="text-gray-500">
                        Real-time assessment for Partner <strong>{partnerId}</strong>
                    </DialogDescription>
                </DialogHeader>

                <div className="min-h-[300px] py-4">
                    {loading ? (
                        <div className="flex flex-col items-center justify-center h-64 space-y-4 text-gray-400">
                            <Loader2 className="w-10 h-10 animate-spin text-deriv-red/50" />
                            <p className="text-sm font-medium animate-pulse">Analyzing trading patterns & interactions...</p>
                        </div>
                    ) : analysis ? (
                        <div className="space-y-6">
                            {/* Analysis Section */}
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="bg-gray-50 p-4 rounded-xl border border-gray-100"
                            >
                                <div className="flex items-center gap-2 mb-2">
                                    <Sparkles className="w-4 h-4 text-purple-600" />
                                    <h4 className="font-bold text-gray-900 text-sm uppercase tracking-wide">GenAI Diagnosis</h4>
                                </div>
                                <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed whitespace-pre-line">
                                    {analysis.explanation}
                                </div>
                            </motion.div>

                            {/* Email Draft Section */}
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 }}
                                className="border border-indigo-100 rounded-xl overflow-hidden"
                            >
                                <div className="bg-indigo-50/50 px-4 py-2 border-b border-indigo-100 flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <Mail className="w-4 h-4 text-indigo-600" />
                                        <span className="font-semibold text-indigo-900 text-sm">Suggested Outreach</span>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={handleCopyEmail}
                                        className="h-7 text-xs hover:bg-white hover:text-indigo-600"
                                    >
                                        {copied ? <CheckCircle className="w-3 h-3 mr-1" /> : <Copy className="w-3 h-3 mr-1" />}
                                        {copied ? "Copied" : "Copy Content"}
                                    </Button>
                                </div>
                                <div className="p-4 bg-white">
                                    <div className="space-y-3">
                                        <div className="text-sm border-b border-gray-50 pb-2">
                                            <span className="text-gray-400 font-medium">Subject:</span> <span className="text-gray-900">{analysis.emailSubject}</span>
                                        </div>
                                        <div className="text-sm text-gray-700 whitespace-pre-wrap font-sans">
                                            {analysis.emailBody}
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        </div>
                    ) : null}
                </div>

                <DialogFooter className="border-t border-gray-100 pt-5 gap-2 sm:gap-0">
                    <Button variant="outline" onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        Dismiss
                    </Button>
                    <div className="flex gap-2 w-full sm:w-auto">
                        <Button className="flex-1 sm:flex-none bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-200">
                            <CheckCircle className="w-4 h-4 mr-2" />
                            Mark as Retained
                        </Button>
                        <Button className="flex-1 sm:flex-none bg-deriv-red hover:bg-deriv-red/90 text-white shadow-lg shadow-deriv-red/20">
                            <Mail className="w-4 h-4 mr-2" />
                            Send Email
                        </Button>
                    </div>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
